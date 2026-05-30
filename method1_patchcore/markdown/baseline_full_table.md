# PatchCore Baseline Reproduction & Efficiency Results (MVTec AD)

- commit: `4592d62` (AUROC) / `4f627c8` (Profile)
- sh / notebook: `method1_patchcore/source/run_baseline.sh` / `method1_patchcore/source/patchcore_colab.ipynb`
- csv: `method1_patchcore/source/results/ (15/15 완료: baseline_{category}.csv)`

> **Environment:** Colab T4 / Python 3.12 / torch 2.x
> **Settings:** PatchCore-10% (WideResNet50, layers 2+3, coreset 0.1, patchsize 3)
> **Parameters:** resize 256, imagesize 224, batch_size 1 (Standard Inference)
> **Paper:** Roth et al. 2022 (PatchCore)

---

## 1. Summary Table: Performance (AUROC)

| Category | I-AUROC (Repro) | I-AUROC (Paper) | Δ (I) | P-AUROC (Repro) | P-AUROC (Paper) | Δ (P) | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| bottle | 1.000 | 1.000 | +0.000 | 0.985 | 0.986 | -0.001 | Done |
| cable | 0.997 | 0.995 | +0.002 | 0.984 | 0.985 | -0.001 | Done |
| capsule | 0.979 | 0.981 | -0.002 | 0.990 | 0.990 | +0.000 | Done |
| carpet | 0.986 | 0.987 | -0.001 | 0.991 | 0.991 | +0.000 | Done |
| grid | 0.979 | 0.979 | +0.000 | 0.988 | 0.987 | +0.001 | Done |
| hazelnut | 1.000 | 1.000 | +0.000 | 0.987 | 0.987 | +0.000 | Done |
| leather | 1.000 | 1.000 | +0.000 | 0.993 | 0.990 | +0.003 | Done |
| metal_nut | 0.999 | 1.000 | -0.001 | 0.983 | 0.991 | -0.008 | Done |
| pill | 0.967 | 0.978 | -0.011 | 0.978 | 0.985 | -0.007 | Done |
| screw | 0.988 | 0.970 | +0.018 | 0.995 | 0.994 | +0.001 | Done |
| tile | 0.995 | 0.989 | +0.006 | 0.957 | 0.959 | -0.002 | Done |
| toothbrush | 1.000 | 0.997 | +0.003 | 0.986 | 0.987 | -0.001 | Done |
| transistor | 0.999 | 1.000 | -0.001 | 0.961 | 0.963 | -0.002 | Done |
| wood | 0.991 | 0.990 | +0.001 | 0.951 | 0.951 | +0.000 | Done |
| zipper | 0.995 | 0.995 | +0.000 | 0.989 | 0.989 | +0.000 | Done |
| **Mean (15개)** | **0.992** | **0.991** | **+0.001** | **0.982** | **0.981** | **+0.001** | **15/15** |

---

## 2. Summary Table: Efficiency (Profiling)

kNN 가속화 연구를 위한 정밀 분석 데이터입니다. (Latency는 이미지당 평균 ms 기준)

| Category | Build Time (sec) | Feat. Ext (ms) | **kNN Search (ms)** | Post-Proc (ms) | **Total Latency** | Peak Mem (MB) | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| bottle | 22.62 | 49.09 | **463.12** | 2.94 | 515.16 | 755.08 | Done |
| cable | 26.38 | 47.71 | **512.28** | 3.05 | 563.04 | 808.40 | Done |
| capsule | 25.22 | 44.69 | **477.06** | 2.89 | 524.64 | 790.97 | Done |
| carpet | 41.49 | 47.13 | **626.06** | 2.98 | 676.17 | 1008.96 | Done |
| grid | 36.22 | 45.11 | **558.96** | 2.99 | 607.06 | 951.50 | Done |
| hazelnut | 79.04 | 46.11 | **868.22** | 2.90 | 917.22 | 1405.80 | Done |
| leather | 31.58 | 46.92 | **543.11** | 2.97 | 593.00 | 882.99 | Done |
| metal_nut | 25.07 | 45.43 | **474.40** | 3.02 | 522.84 | 794.51 | Done |
| pill | 37.19 | 45.88 | **599.81** | 2.93 | 648.62 | 961.58 | Done |
| screw | 52.23 | 45.81 | **693.61** | 2.84 | 742.26 | 1152.09 | Done |
| tile | 27.04 | 46.22 | **508.70** | 3.02 | 557.94 | 829.38 | Done |
| toothbrush | 2.29 | 44.88 | **146.20** | 3.71 | 194.79 | 223.84 | Done |
| transistor | 24.34 | 46.29 | **473.68** | 2.91 | 522.88 | 770.58 | Done |
| wood | 31.76 | 45.59 | **549.07** | 2.91 | 597.57 | 889.91 | Done |
| zipper | 31.12 | 46.30 | **597.95** | 3.30 | 647.55 | 866.06 | Done |
| **Mean (15개)** | **32.91** | **46.29** | **539.48** | **3.02** | **588.78** | **873.34** | **15/15** |

---

## 3. 주요 관찰 사항 (Profiling Insights)

### 3.1. 런타임 병목 구조 분석
*   **kNN Search의 절대적 비중**: `bottle`에서 89.9%, `hazelnut`에서 **94.7%**가 kNN 탐색에 소요됩니다. 이는 백본의 Feature Extraction(약 46-49ms) 대비 **10-19배** 긴 시간입니다.
*   **스케일 가변성**: 학습 이미지 수가 209개(`bottle`)에서 391개(`hazelnut`)로 약 1.8배 증가할 때, kNN 지연 시간은 약 **1.87배** 증가하여 선형적인 복잡도 증가를 보입니다.

### 3.2. 메모리 및 빌드 효율성
*   **Memory Bank Build Overhead**: 전체 학습 과정에서 Coreset Sampling 및 Bank 구축이 Feature Extraction보다 더 많은 시간(hazelnut 기준 2.2배)을 소요합니다.
*   **메모리 점유**: Peak Memory의 대부분이 `faiss` 인덱스 또는 raw memory bank tensor에 의해 점유되며, `hazelnut` 기준 1.4GB는 대규모 데이터셋 확장 시 GPU 메모리 부족(OOM)의 잠재적 위험 요소입니다.

### 3.3. 가속화 전략 제언
*   **IVF/HNSW 도입 필요성**: 현재의 Linear Search(Flat Index)는 O(N) 복잡도를 가지므로, 대규모 데이터셋에서도 상수의 탐색 시간을 보장하는 Approximate Nearest Neighbor(ANN) 기법 도입이 필수적입니다.
*   **PQ(Product Quantization)**: 메모리 점유율을 1/4 이하로 압축하면서도 성능 하락을 최소화하는 양자화 기법이 `hazelnut`과 같은 대용량 카테고리에 유효할 것으로 판단됩니다.
