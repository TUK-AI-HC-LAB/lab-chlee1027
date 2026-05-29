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

| Category | kNN Search Ratio | kNN Latency (per img) | Memory Bank Peak Memory | Status |
| :--- | :---: | :---: | :---: | :---: |
| bottle | **89.9%** | **463.12 ms** | **755.08 MB** | Done |
| cable | **91.0%** | **512.28 ms** | **808.40 MB** | Done |
| capsule | **90.9%** | **477.06 ms** | **790.97 MB** | Done |
| carpet | **92.6%** | **626.06 ms** | **1008.96 MB** | Done |
| grid | **92.1%** | **558.96 ms** | **951.50 MB** | Done |
| hazelnut | **94.7%** | **868.22 ms** | **1405.80 MB** | Done |
| leather | **91.6%** | **543.11 ms** | **882.99 MB** | Done |
| metal_nut | **90.7%** | **474.40 ms** | **794.51 MB** | Done |
| pill | **92.5%** | **599.81 ms** | **961.58 MB** | Done |
| screw | **93.4%** | **693.61 ms** | **1152.09 MB** | Done |
| tile | **91.2%** | **508.70 ms** | **829.38 MB** | Done |
| toothbrush | **75.1%** | **146.20 ms** | **223.84 MB** | Done |
| transistor | **90.6%** | **473.68 ms** | **770.58 MB** | Done |
| wood | **91.9%** | **549.07 ms** | **889.91 MB** | Done |
| zipper | **92.3%** | **597.95 ms** | **866.06 MB** | Done |
| **Mean (15개)** | **90.8%** | **539.48 ms** | **873.34 MB** | **15/15** |

---

## 3. 주요 관찰 사항 (Profiling Insights)

*   **kNN Search 병목의 지배성**: 15개 카테고리 평균 **90.8%**의 런타임이 kNN 탐색에 집중되어 있어 실시간 가속의 최우선 타겟임을 실증함.
*   **데이터 스케일 영향**: `hazelnut` 등 학습 셋이 클수록 kNN 지연 시간(868.22ms)과 메모리 점유(1.4GB)가 선형 비례하여 증가함.
