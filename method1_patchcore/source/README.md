# method1_patchcore — 실행 가이드

PatchCore (Roth et al. 2022) baseline을 MVTec AD에서 재현하기 위한 source 디렉토리입니다.

## 환경 (Colab T4 기준)

- Python 3.12, CUDA 12.x
- PyTorch 2.10.0+cu128 (Colab 기본)
- faiss-cpu 1.13.2

`requirements.txt` 참고. Colab 기본 환경에선 `faiss-cpu`만 추가 설치하면 됩니다.

## 데이터 준비

MVTec AD를 다음 구조로 두세요.

```
<MVTEC_DIR>/
├── bottle/
│   ├── train/good/...
│   └── test/{good,broken_large,...}/...
├── leather/
└── ...
```

Colab에선 Google Drive 마운트 후 `/content/drive/MyDrive/anormaly_detection/mvtec` 사용. 로컬에서는 임의 경로에 두고 `MVTEC_DIR` 환경변수로 지정.

## 실행

```bash
# bottle
CATEGORY=bottle MVTEC_DIR=/path/to/mvtec bash run_baseline.sh

# leather
CATEGORY=leather MVTEC_DIR=/path/to/mvtec bash run_baseline.sh
```

스크립트가 하는 일:

1. upstream [amazon-science/patchcore-inspection](https://github.com/amazon-science/patchcore-inspection) 을 `${PATCHCORE_DIR:-$HOME/patchcore-inspection}` 에 clone (이미 있으면 skip)
2. 본 repo의 수정사항을 upstream의 `bin/run_patchcore.py` 에 적용
   - 기본 동작: `source/run_patchcore.py` (수정본 전체 파일)이 있으므로 그걸로 덮어쓰기
   - fallback: 위 파일이 없을 경우 `apply_modifications.py` 가 idempotent하게 패치 적용 (upstream 코드 변경 시 대비)
3. 표준 PatchCore-10% 설정으로 실행 (WRN-50, layer2+3, coreset 10%, NN=1, patchsize=3, resize 256/center 224, seed 0)
4. 결과는 upstream repo 안의 `${RESULT_NAME:-results_<CATEGORY>}/` 에 저장. 메트릭 csv는 본 repo의 `results/baseline_<CATEGORY>_<DATE>.csv` 로 옮겨두세요.

## 수정 내역 (upstream `bin/run_patchcore.py` 대비)

`run_patchcore.py` 안의 `image_transform()` 함수만 수정. 시각화 시 dataset attribute 접근이 실패해서 ImageNet 표준값으로 대체.

**원본**:
```python
def image_transform(image):
    in_std = np.array(
        dataloaders["testing"].dataset.transform_std
    ).reshape(-1, 1, 1)
    in_mean = np.array(
        dataloaders["testing"].dataset.transform_mean
    ).reshape(-1, 1, 1)
    image = dataloaders["testing"].dataset.transform_img(image)
    return np.clip(
        (image.numpy() * in_std + in_mean) * 255, 0, 255
    ).astype(np.uint8)
```

**수정 후** (실제 `source/run_patchcore.py` 내 형태):
```python
def image_transform(image):
    in_std = np.array([0.229, 0.224, 0.225]).reshape(-1, 1, 1)
    in_mean = np.array([0.485, 0.456, 0.406]).reshape(-1, 1, 1)

    image = dataloaders["testing"].dataset.transform_img(image)

    return np.clip((image.numpy() * in_std + in_mean) * 255, 0, 255).astype(np.uint8)
```

이 변경은 segmentation 시각화 이미지 생성에만 영향. evaluation 메트릭(I-AUROC, P-AUROC) 계산 경로는 건드리지 않음.

## 재현 출처 (가이드 형식 — commit/sh/csv 3줄)

bottle:
- commit: TBD (이 repo에서 baseline 실행 시점 commit hash 채울 것)
- sh: `method1_patchcore/source/run_baseline.sh` (CATEGORY=bottle)
- csv: `method1_patchcore/source/results/baseline_bottle_20260506.csv`

leather:
- commit: TBD
- sh: `method1_patchcore/source/run_baseline.sh` (CATEGORY=leather)
- csv: `method1_patchcore/source/results/baseline_leather_20260506.csv`

원본 Colab 노트북: `method1_patchcore/source/patchcore_colab.ipynb`
