import faiss
import numpy as np
import torch
from patchcore.common import FaissNN

class FaissIVF(FaissNN):
    def __init__(self, nlist=100, nprobe=10, on_gpu=False, num_workers=4):
        super().__init__(on_gpu, num_workers)
        self.nlist = nlist
        self.nprobe = nprobe

    def _create_index(self, dimension):
        # IVF Index requires a quantizer (usually IndexFlatL2)
        quantizer = faiss.IndexFlatL2(dimension)
        index = faiss.IndexIVFFlat(quantizer, dimension, self.nlist, faiss.METRIC_L2)
        return self._index_to_gpu(index)

    def _train(self, index, features):
        # IVF must be trained on the data to form clusters
        if not index.is_trained:
            index.train(features)
        index.nprobe = self.nprobe

class FaissHNSW(FaissNN):
    def __init__(self, M=32, efSearch=64, on_gpu=False, num_workers=4):
        super().__init__(on_gpu, num_workers)
        self.M = M
        self.efSearch = efSearch

    def _create_index(self, dimension):
        # HNSW index
        index = faiss.IndexHNSWFlat(dimension, self.M)
        index.hnsw.efSearch = self.efSearch
        # HNSW on GPU is typically achieved via GpuIndexFlatL2 cloner, 
        # but native HNSW is CPU only. faiss.index_cpu_to_gpu works.
        return self._index_to_gpu(index)

class FaissPQ(FaissNN):
    def __init__(self, m=32, nbits=8, on_gpu=False, num_workers=4):
        super().__init__(on_gpu, num_workers)
        self.m = m
        self.nbits = nbits

    def _create_index(self, dimension):
        # Product Quantization index
        index = faiss.IndexPQ(dimension, self.m, self.nbits)
        return self._index_to_gpu(index)

    def _train(self, index, features):
        # PQ must be trained to learn the codebooks
        if not index.is_trained:
            index.train(features)
