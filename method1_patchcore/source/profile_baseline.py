import contextlib
import logging
import os
import sys
import time
import gc
import csv
import types

import click
import numpy as np
import torch
import tqdm
import psutil

import patchcore.backbones
import patchcore.common
import patchcore.metrics
import patchcore.patchcore
import patchcore.sampler
import patchcore.utils

LOGGER = logging.getLogger(__name__)

_DATASETS = {"mvtec": ["patchcore.datasets.mvtec", "MVTecDataset"]}


class Profiler:
    def __init__(self, device):
        self.device = device
        self.is_cuda = "cuda" in str(device).lower()
        self.stats = {
            "train_feat_extraction_time": 0.0,
            "train_feat_extraction_mem": 0.0,
            "memory_bank_build_time": 0.0,
            "memory_bank_build_mem": 0.0,
            "test_feat_extraction_time": 0.0,
            "test_feat_extraction_mem": 0.0,
            "knn_search_time": 0.0,
            "knn_search_mem": 0.0,
            "post_processing_time": 0.0,
            "post_processing_mem": 0.0,
        }
        
    def reset_memory(self):
        if self.is_cuda:
            torch.cuda.empty_cache()
            torch.cuda.reset_peak_memory_stats()
            gc.collect()
            
    def get_peak_memory(self):
        if self.is_cuda:
            return torch.cuda.max_memory_allocated(self.device) / (1024 * 1024) # in MB
        else:
            process = psutil.Process(os.getpid())
            return process.memory_info().rss / (1024 * 1024) # in MB


def make_profiled_fill_memory_bank(original_fill_memory_bank, profiler):
    def profiled_fill_memory_bank(self, input_data):
        _ = self.forward_modules.eval()

        def _image_to_features(input_image):
            with torch.no_grad():
                input_image = input_image.to(torch.float).to(self.device)
                return self._embed(input_image)

        # Profile Training Feature Extraction
        profiler.reset_memory()
        start_time = time.perf_counter()
        start_mem = profiler.get_peak_memory()
        
        features = []
        with tqdm.tqdm(
            input_data, desc="Computing support features...", position=1, leave=False
        ) as data_iterator:
            for image in data_iterator:
                if isinstance(image, dict):
                    image = image["image"]
                features.append(_image_to_features(image))
                
        profiler.stats["train_feat_extraction_time"] = time.perf_counter() - start_time
        profiler.stats["train_feat_extraction_mem"] = profiler.get_peak_memory() - start_mem
        if profiler.stats["train_feat_extraction_mem"] < 0:
            profiler.stats["train_feat_extraction_mem"] = 0.0

        # Profile Memory Bank Build
        profiler.reset_memory()
        start_time = time.perf_counter()
        start_mem = profiler.get_peak_memory()
        
        features = np.concatenate(features, axis=0)
        features = self.featuresampler.run(features)

        self.anomaly_scorer.fit(detection_features=[features])
        
        profiler.stats["memory_bank_build_time"] = time.perf_counter() - start_time
        profiler.stats["memory_bank_build_mem"] = profiler.get_peak_memory() - start_mem
        if profiler.stats["memory_bank_build_mem"] < 0:
            profiler.stats["memory_bank_build_mem"] = 0.0
            
    return profiled_fill_memory_bank


def make_profiled_predict(original_predict, profiler):
    def profiled_predict(self, images):
        images = images.to(torch.float).to(self.device)
        _ = self.forward_modules.eval()

        batchsize = images.shape[0]
        with torch.no_grad():
            # 1. Feature Extraction (Test)
            profiler.reset_memory()
            t0 = time.perf_counter()
            m0 = profiler.get_peak_memory()
            
            features, patch_shapes = self._embed(images, provide_patch_shapes=True)
            features = np.asarray(features)
            
            profiler.stats["test_feat_extraction_time"] += (time.perf_counter() - t0)
            mem_diff = profiler.get_peak_memory() - m0
            if mem_diff > profiler.stats["test_feat_extraction_mem"]:
                profiler.stats["test_feat_extraction_mem"] = mem_diff

            # 2. kNN Search
            profiler.reset_memory()
            t0 = time.perf_counter()
            m0 = profiler.get_peak_memory()
            
            patch_scores = image_scores = self.anomaly_scorer.predict([features])[0]
            
            profiler.stats["knn_search_time"] += (time.perf_counter() - t0)
            mem_diff = profiler.get_peak_memory() - m0
            if mem_diff > profiler.stats["knn_search_mem"]:
                profiler.stats["knn_search_mem"] = mem_diff

            # 3. Post-processing
            profiler.reset_memory()
            t0 = time.perf_counter()
            m0 = profiler.get_peak_memory()
            
            image_scores = self.patch_maker.unpatch_scores(
                image_scores, batchsize=batchsize
            )
            image_scores = image_scores.reshape(*image_scores.shape[:2], -1)
            image_scores = self.patch_maker.score(image_scores)

            patch_scores = self.patch_maker.unpatch_scores(
                patch_scores, batchsize=batchsize
            )
            scales = patch_shapes[0]
            patch_scores = patch_scores.reshape(batchsize, scales[0], scales[1])

            masks = self.anomaly_segmentor.convert_to_segmentation(patch_scores)
            
            profiler.stats["post_processing_time"] += (time.perf_counter() - t0)
            mem_diff = profiler.get_peak_memory() - m0
            if mem_diff > profiler.stats["post_processing_mem"]:
                profiler.stats["post_processing_mem"] = mem_diff

        return [score for score in image_scores], [mask for mask in masks]
        
    return profiled_predict


@click.group(chain=True)
@click.argument("results_path", type=str)
@click.option("--gpu", type=int, default=[0], multiple=True, show_default=True)
@click.option("--seed", type=int, default=0, show_default=True)
@click.option("--log_group", type=str, default="group")
@click.option("--log_project", type=str, default="project")
@click.option("--save_segmentation_images", is_flag=True)
@click.option("--save_patchcore_model", is_flag=True)
def main(**kwargs):
    pass


@main.result_callback()
def run(
    methods,
    results_path,
    gpu,
    seed,
    log_group,
    log_project,
    save_segmentation_images,
    save_patchcore_model,
):
    methods = {key: item for (key, item) in methods}

    run_save_path = patchcore.utils.create_storage_folder(
        results_path, log_project, log_group, mode="iterate"
    )

    list_of_dataloaders = methods["get_dataloaders"](seed)

    device = patchcore.utils.set_torch_device(gpu)
    device_context = (
        torch.cuda.device("cuda:{}".format(device.index))
        if "cuda" in device.type.lower()
        else contextlib.suppress()
    )

    result_collect = []

    for dataloader_count, dataloaders in enumerate(list_of_dataloaders):
        LOGGER.info(
            "Evaluating dataset [{}] ({}/{})...".format(
                dataloaders["training"].name,
                dataloader_count + 1,
                len(list_of_dataloaders),
            )
        )

        patchcore.utils.fix_seeds(seed, device)

        dataset_name = dataloaders["training"].name

        with device_context:
            torch.cuda.empty_cache()
            imagesize = dataloaders["training"].dataset.imagesize
            sampler = methods["get_sampler"](
                device,
            )
            PatchCore_list = methods["get_patchcore"](imagesize, sampler, device)
            
            # Create the Profiler
            profiler = Profiler(device)
            
            # Monkeypatch the fit and predict methods of each PatchCore instance
            for PatchCore in PatchCore_list:
                PatchCore._fill_memory_bank = types.MethodType(
                    make_profiled_fill_memory_bank(PatchCore._fill_memory_bank, profiler),
                    PatchCore
                )
                PatchCore._predict = types.MethodType(
                    make_profiled_predict(PatchCore._predict, profiler),
                    PatchCore
                )

            if len(PatchCore_list) > 1:
                LOGGER.info(
                    "Utilizing PatchCore Ensemble (N={}).".format(len(PatchCore_list))
                )
            for i, PatchCore in enumerate(PatchCore_list):
                torch.cuda.empty_cache()
                if PatchCore.backbone.seed is not None:
                    patchcore.utils.fix_seeds(PatchCore.backbone.seed, device)
                LOGGER.info(
                    "Training models ({}/{})".format(i + 1, len(PatchCore_list))
                )
                torch.cuda.empty_cache()
                PatchCore.fit(dataloaders["training"])

            torch.cuda.empty_cache()
            aggregator = {"scores": [], "segmentations": []}
            for i, PatchCore in enumerate(PatchCore_list):
                torch.cuda.empty_cache()
                LOGGER.info(
                    "Embedding test data with models ({}/{})".format(
                        i + 1, len(PatchCore_list)
                    )
                )
                scores, segmentations, labels_gt, masks_gt = PatchCore.predict(
                    dataloaders["testing"]
                )
                aggregator["scores"].append(scores)
                aggregator["segmentations"].append(segmentations)

            scores = np.array(aggregator["scores"])
            min_scores = scores.min(axis=-1).reshape(-1, 1)
            max_scores = scores.max(axis=-1).reshape(-1, 1)
            scores = (scores - min_scores) / (max_scores - min_scores)
            scores = np.mean(scores, axis=0)

            segmentations = np.array(aggregator["segmentations"])
            min_scores = (
                segmentations.reshape(len(segmentations), -1)
                .min(axis=-1)
                .reshape(-1, 1, 1, 1)
            )
            max_scores = (
                segmentations.reshape(len(segmentations), -1)
                .max(axis=-1)
                .reshape(-1, 1, 1, 1)
            )
            segmentations = (segmentations - min_scores) / (max_scores - min_scores)
            segmentations = np.mean(segmentations, axis=0)

            anomaly_labels = [
                x[1] != "good" for x in dataloaders["testing"].dataset.data_to_iterate
            ]

            # (Optional) Plot example images.
            if save_segmentation_images:
                image_paths = [
                    x[2] for x in dataloaders["testing"].dataset.data_to_iterate
                ]
                mask_paths = [
                    x[3] for x in dataloaders["testing"].dataset.data_to_iterate
                ]

                def image_transform(image):
                    in_std = np.array([0.229, 0.224, 0.225]).reshape(-1, 1, 1)
                    in_mean = np.array([0.485, 0.456, 0.406]).reshape(-1, 1, 1)
                
                    image = dataloaders["testing"].dataset.transform_img(image)

                    return np.clip((image.numpy() * in_std + in_mean) * 255, 0, 255).astype(np.uint8)

                def mask_transform(mask):
                    return dataloaders["testing"].dataset.transform_mask(mask).numpy()

                image_save_path = os.path.join(
                    run_save_path, "segmentation_images", dataset_name
                )
                os.makedirs(image_save_path, exist_ok=True)
                patchcore.utils.plot_segmentation_images(
                    image_save_path,
                    image_paths,
                    segmentations,
                    scores,
                    mask_paths,
                    image_transform=image_transform,
                    mask_transform=mask_transform,
                )

            LOGGER.info("Computing evaluation metrics.")
            auroc = patchcore.metrics.compute_imagewise_retrieval_metrics(
                scores, anomaly_labels
            )["auroc"]

            # Compute PRO score & PW Auroc for all images
            pixel_scores = patchcore.metrics.compute_pixelwise_retrieval_metrics(
                segmentations, masks_gt
            )
            full_pixel_auroc = pixel_scores["auroc"]

            # Compute PRO score & PW Auroc only images with anomalies
            sel_idxs = []
            for i in range(len(masks_gt)):
                if np.sum(masks_gt[i]) > 0:
                    sel_idxs.append(i)
            pixel_scores = patchcore.metrics.compute_pixelwise_retrieval_metrics(
                [segmentations[i] for i in sel_idxs],
                [masks_gt[i] for i in sel_idxs],
            )
            anomaly_pixel_auroc = pixel_scores["auroc"]

            result_collect.append(
                {
                    "dataset_name": dataset_name,
                    "instance_auroc": auroc,
                    "full_pixel_auroc": full_pixel_auroc,
                    "anomaly_pixel_auroc": anomaly_pixel_auroc,
                }
            )

            for key, item in result_collect[-1].items():
                if key != "dataset_name":
                    LOGGER.info("{0}: {1:3.3f}".format(key, item))

            # (Optional) Store PatchCore model for later re-use.
            if save_patchcore_model:
                patchcore_save_path = os.path.join(
                    run_save_path, "models", dataset_name
                )
                os.makedirs(patchcore_save_path, exist_ok=True)
                for i, PatchCore in enumerate(PatchCore_list):
                    prepend = (
                        "Ensemble-{}-{}_".format(i + 1, len(PatchCore_list))
                        if len(PatchCore_list) > 1
                        else ""
                    )
                    PatchCore.save_to_path(patchcore_save_path, prepend)

            # Collect and log profiling metrics
            num_train = len(dataloaders["training"].dataset)
            num_test = len(dataloaders["testing"].dataset)
            
            train_feat_time = profiler.stats["train_feat_extraction_time"]
            train_feat_mem = profiler.stats["train_feat_extraction_mem"]
            mb_build_time = profiler.stats["memory_bank_build_time"]
            mb_build_mem = profiler.stats["memory_bank_build_mem"]
            
            test_feat_time = profiler.stats["test_feat_extraction_time"]
            test_feat_mem = profiler.stats["test_feat_extraction_mem"]
            test_feat_time_per_img = (test_feat_time / num_test) * 1000.0 if num_test > 0 else 0.0
            
            knn_time = profiler.stats["knn_search_time"]
            knn_mem = profiler.stats["knn_search_mem"]
            knn_time_per_img = (knn_time / num_test) * 1000.0 if num_test > 0 else 0.0
            
            post_time = profiler.stats["post_processing_time"]
            post_mem = profiler.stats["post_processing_mem"]
            post_time_per_img = (post_time / num_test) * 1000.0 if num_test > 0 else 0.0
            
            total_inf_time = test_feat_time + knn_time + post_time
            total_inf_time_per_img = (total_inf_time / num_test) * 1000.0 if num_test > 0 else 0.0
            
            LOGGER.info(f"\n==========================================")
            LOGGER.info(f"--- Profiling Results for {dataset_name} ---")
            LOGGER.info(f"Num Train Images: {num_train}, Num Test Images: {num_test}")
            LOGGER.info(f"Train Feature Extraction: {train_feat_time:.4f} s | {train_feat_mem:.4f} MB")
            LOGGER.info(f"Memory Bank Build:        {mb_build_time:.4f} s | {mb_build_mem:.4f} MB")
            LOGGER.info(f"Test Feature Extraction:  {test_feat_time:.4f} s ({test_feat_time_per_img:.2f} ms/img) | {test_feat_mem:.4f} MB")
            LOGGER.info(f"kNN Search:               {knn_time:.4f} s ({knn_time_per_img:.2f} ms/img) | {knn_mem:.4f} MB")
            LOGGER.info(f"Post-processing:          {post_time:.4f} s ({post_time_per_img:.2f} ms/img) | {post_mem:.4f} MB")
            LOGGER.info(f"Total Test Inference:     {total_inf_time:.4f} s ({total_inf_time_per_img:.2f} ms/img)")
            LOGGER.info(f"==========================================\n")
            
            # Save to baseline_profile_results.csv in the results folder
            # 1) In the execution results folder
            csv_dir1 = os.path.join(run_save_path, "results")
            os.makedirs(csv_dir1, exist_ok=True)
            csv_path1 = os.path.join(csv_dir1, "baseline_profile_results.csv")
            
            # 2) In the original method1_patchcore/source/results directory
            # Make sure to resolve absolute path of currently executing script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            csv_dir2 = os.path.join(script_dir, "results")
            os.makedirs(csv_dir2, exist_ok=True)
            csv_path2 = os.path.join(csv_dir2, "baseline_profile_results.csv")
            
            header = [
                "Category",
                "Num_Train_Images",
                "Num_Test_Images",
                "Train_FeatExtraction_Time_sec",
                "Train_FeatExtraction_PeakMem_MB",
                "MemoryBankBuild_Time_sec",
                "MemoryBankBuild_PeakMem_MB",
                "Test_FeatExtraction_Time_sec",
                "Test_FeatExtraction_PeakMem_MB",
                "Test_FeatExtraction_TimePerImage_ms",
                "kNN_Search_Time_sec",
                "kNN_Search_PeakMem_MB",
                "kNN_Search_TimePerImage_ms",
                "PostProcessing_Time_sec",
                "PostProcessing_PeakMem_MB",
                "PostProcessing_TimePerImage_ms",
                "Total_Inference_Time_sec",
                "Total_Inference_TimePerImage_ms"
            ]
            
            row = [
                dataset_name.split("_")[-1] if "_" in dataset_name else dataset_name,
                num_train,
                num_test,
                train_feat_time,
                train_feat_mem,
                mb_build_time,
                mb_build_mem,
                test_feat_time,
                test_feat_mem,
                test_feat_time_per_img,
                knn_time,
                knn_mem,
                knn_time_per_img,
                post_time,
                post_mem,
                post_time_per_img,
                total_inf_time,
                total_inf_time_per_img
            ]
            
            def write_csv(path):
                rows_to_keep = []
                if os.path.exists(path):
                    try:
                        with open(path, "r", newline="", encoding="utf-8") as f:
                            reader = csv.reader(f)
                            existing_header = next(reader, None)
                            for r in reader:
                                if r and r[0] != row[0]:
                                    rows_to_keep.append(r)
                    except Exception:
                        pass
                
                with open(path, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(header)
                    for r in rows_to_keep:
                        writer.writerow(r)
                    writer.writerow(row)
            
            write_csv(csv_path1)
            write_csv(csv_path2)

        LOGGER.info("\n\n-----\n")

    # Store all results and mean scores to a csv-file.
    result_metric_names = list(result_collect[-1].keys())[1:]
    result_dataset_names = [results["dataset_name"] for results in result_collect]
    result_scores = [list(results.values())[1:] for results in result_collect]
    patchcore.utils.compute_and_store_final_results(
        run_save_path,
        result_scores,
        column_names=result_metric_names,
        row_names=result_dataset_names,
    )


@main.command("patch_core")
@click.option("--backbone_names", "-b", type=str, multiple=True, default=[])
@click.option("--layers_to_extract_from", "-le", type=str, multiple=True, default=[])
@click.option("--pretrain_embed_dimension", type=int, default=1024)
@click.option("--target_embed_dimension", type=int, default=1024)
@click.option("--preprocessing", type=click.Choice(["mean", "conv"]), default="mean")
@click.option("--aggregation", type=click.Choice(["mean", "mlp"]), default="mean")
@click.option("--anomaly_scorer_num_nn", type=int, default=5)
@click.option("--patchsize", type=int, default=3)
@click.option("--patchscore", type=str, default="max")
@click.option("--patchoverlap", type=float, default=0.0)
@click.option("--patchsize_aggregate", "-pa", type=int, multiple=True, default=[])
@click.option("--faiss_on_gpu", is_flag=True)
@click.option("--faiss_num_workers", type=int, default=8)
def patch_core(
    backbone_names,
    layers_to_extract_from,
    pretrain_embed_dimension,
    target_embed_dimension,
    preprocessing,
    aggregation,
    patchsize,
    patchscore,
    patchoverlap,
    anomaly_scorer_num_nn,
    patchsize_aggregate,
    faiss_on_gpu,
    faiss_num_workers,
):
    backbone_names = list(backbone_names)
    if len(backbone_names) > 1:
        layers_to_extract_from_coll = [[] for _ in range(len(backbone_names))]
        for layer in layers_to_extract_from:
            idx = int(layer.split(".")[0])
            layer = ".".join(layer.split(".")[1:])
            layers_to_extract_from_coll[idx].append(layer)
    else:
        layers_to_extract_from_coll = [layers_to_extract_from]

    def get_patchcore(input_shape, sampler, device):
        loaded_patchcores = []
        for backbone_name, layers_to_extract_from in zip(
            backbone_names, layers_to_extract_from_coll
        ):
            backbone_seed = None
            if ".seed-" in backbone_name:
                backbone_name, backbone_seed = backbone_name.split(".seed-")[0], int(
                    backbone_name.split("-")[-1]
                )
            backbone = patchcore.backbones.load(backbone_name)
            backbone.name, backbone.seed = backbone_name, backbone_seed

            nn_method = patchcore.common.FaissNN(faiss_on_gpu, faiss_num_workers)

            patchcore_instance = patchcore.patchcore.PatchCore(device)
            patchcore_instance.load(
                backbone=backbone,
                layers_to_extract_from=layers_to_extract_from,
                device=device,
                input_shape=input_shape,
                pretrain_embed_dimension=pretrain_embed_dimension,
                target_embed_dimension=target_embed_dimension,
                patchsize=patchsize,
                featuresampler=sampler,
                anomaly_scorer_num_nn=anomaly_scorer_num_nn,
                nn_method=nn_method,
            )
            loaded_patchcores.append(patchcore_instance)
        return loaded_patchcores

    return ("get_patchcore", get_patchcore)


@main.command("sampler")
@click.argument("name", type=str)
@click.option("--percentage", "-p", type=float, default=0.1, show_default=True)
def sampler(name, percentage):
    def get_sampler(device):
        if name == "identity":
            return patchcore.sampler.IdentitySampler()
        elif name == "greedy_coreset":
            return patchcore.sampler.GreedyCoresetSampler(percentage, device)
        elif name == "approx_greedy_coreset":
            return patchcore.sampler.ApproximateGreedyCoresetSampler(percentage, device)

    return ("get_sampler", get_sampler)


@main.command("dataset")
@click.argument("name", type=str)
@click.argument("data_path", type=click.Path(exists=True, file_okay=False))
@click.option("--subdatasets", "-d", multiple=True, type=str, required=True)
@click.option("--train_val_split", type=float, default=1, show_default=True)
@click.option("--batch_size", default=2, type=int, show_default=True)
@click.option("--num_workers", default=8, type=int, show_default=True)
@click.option("--resize", default=256, type=int, show_default=True)
@click.option("--imagesize", default=224, type=int, show_default=True)
@click.option("--augment", is_flag=True)
def dataset(
    name,
    data_path,
    subdatasets,
    train_val_split,
    batch_size,
    resize,
    imagesize,
    num_workers,
    augment,
):
    dataset_info = _DATASETS[name]
    dataset_library = __import__(dataset_info[0], fromlist=[dataset_info[1]])

    def get_dataloaders(seed):
        dataloaders = []
        for subdataset in subdatasets:
            train_dataset = dataset_library.__dict__[dataset_info[1]](
                data_path,
                classname=subdataset,
                resize=resize,
                train_val_split=train_val_split,
                imagesize=imagesize,
                split=dataset_library.DatasetSplit.TRAIN,
                seed=seed,
                augment=augment,
            )

            test_dataset = dataset_library.__dict__[dataset_info[1]](
                data_path,
                classname=subdataset,
                resize=resize,
                imagesize=imagesize,
                split=dataset_library.DatasetSplit.TEST,
                seed=seed,
            )

            train_dataloader = torch.utils.data.DataLoader(
                train_dataset,
                batch_size=batch_size,
                shuffle=False,
                num_workers=num_workers,
                pin_memory=True,
            )

            test_dataloader = torch.utils.data.DataLoader(
                test_dataset,
                batch_size=batch_size,
                shuffle=False,
                num_workers=num_workers,
                pin_memory=True,
            )

            train_dataloader.name = name
            if subdataset is not None:
                train_dataloader.name += "_" + subdataset

            if train_val_split < 1:
                val_dataset = dataset_library.__dict__[dataset_info[1]](
                    data_path,
                    classname=subdataset,
                    resize=resize,
                    train_val_split=train_val_split,
                    imagesize=imagesize,
                    split=dataset_library.DatasetSplit.VAL,
                    seed=seed,
                )

                val_dataloader = torch.utils.data.DataLoader(
                    val_dataset,
                    batch_size=batch_size,
                    shuffle=False,
                    num_workers=num_workers,
                    pin_memory=True,
                )
            else:
                val_dataloader = None
            dataloader_dict = {
                "training": train_dataloader,
                "validation": val_dataloader,
                "testing": test_dataloader,
            }

            dataloaders.append(dataloader_dict)
        return dataloaders

    return ("get_dataloaders", get_dataloaders)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    LOGGER.info("Command line arguments: {}".format(" ".join(sys.argv)))
    main()
