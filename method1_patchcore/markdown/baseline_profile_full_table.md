# PatchCore Baseline Profiling Results (MVTec AD)

- commit: `4f627c8`
- sh / notebook: `method1_patchcore/source/profile_colab.ipynb`
- csv: `method1_patchcore/source/results/baseline_profile_results.csv (15/15 완료: bottle, cable, capsule, carpet, grid, hazelnut, leather, metal_nut, pill, screw, tile, toothbrush, transistor, wood, zipper)`

> **Environment:** Colab T4 / Python 3.12 / torch 2.x
> **Settings:** PatchCore-10% (WideResNet50, layers 2+3, coreset 0.1, patchsize 3)
> **Parameters:** resize 256, imagesize 224, batch_size 1 (Standard Inference)
> **Paper:** Roth et al. 2022 (PatchCore)

---

## 1. Profiling Summary Table (15 Categories)

| Category | Train Images | Test Images | I-AUROC | P-AUROC | kNN Search Ratio | kNN Latency (per img) | Memory Bank Peak Memory | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| bottle | 209장 | 83장 | 1.000 | 0.985 | **89.9% (38.44s)** | **463.12 ms** | **755.08 MB** | Done |
| cable | 224장 | 150장 | 0.997 | 0.984 | **91.0% (76.84s)** | **512.28 ms** | **808.40 MB** | Done |
| capsule | 219장 | 132장 | 0.979 | 0.990 | **90.9% (62.97s)** | **477.06 ms** | **790.97 MB** | Done |
| carpet | 280장 | 117장 | 0.986 | 0.991 | **92.6% (73.25s)** | **626.06 ms** | **1008.96 MB** | Done |
| grid | 264장 | 78장 | 0.979 | 0.988 | **92.1% (43.60s)** | **558.96 ms** | **951.50 MB** | Done |
| hazelnut | 391장 | 110장 | 1.000 | 0.987 | **94.7% (95.50s)** | **868.22 ms** | **1405.80 MB** | Done |
| leather | 245장 | 124장 | 1.000 | 0.993 | **91.6% (67.35s)** | **543.11 ms** | **882.99 MB** | Done |
| metal_nut | 220장 | 115장 | 0.999 | 0.983 | **90.7% (54.56s)** | **474.40 ms** | **794.51 MB** | Done |
| pill | 267장 | 167장 | 0.967 | 0.978 | **92.5% (100.17s)** | **599.81 ms** | **961.58 MB** | Done |
| screw | 320장 | 160장 | 0.988 | 0.995 | **93.4% (110.98s)** | **693.61 ms** | **1152.09 MB** | Done |
| tile | 230장 | 117장 | 0.995 | 0.957 | **91.2% (59.52s)** | **508.70 ms** | **829.38 MB** | Done |
| toothbrush | 60장 | 42장 | 1.000 | 0.986 | **75.1% (6.14s)** | **146.20 ms** | **223.84 MB** | Done |
| transistor | 213장 | 100장 | 0.999 | 0.961 | **90.6% (47.37s)** | **473.68 ms** | **770.58 MB** | Done |
| wood | 247장 | 79장 | 0.991 | 0.951 | **91.9% (43.38s)** | **549.07 ms** | **889.91 MB** | Done |
| zipper | 240장 | 151장 | 0.995 | 0.989 | **92.3% (90.29s)** | **597.95 ms** | **866.06 MB** | Done |
| **Mean (15개)** | **228.6장** | **115.0장** | **0.992** | **0.982** | **90.8%** | **539.48 ms** | **873.34 MB** | **15/15** |

---

## 2. 주요 관찰 사항 (Profiling Insights)

*   **kNN Search 병목의 지배성**:
    *   15개 카테고리 전체의 kNN Search 시간 비율 평균은 **90.8%**에 달합니다. 
    *   즉, 이미지당 평균 약 **539.48 ms**의 추론 시간 중 대부분이 kNN Search 단계에 고정적으로 종속되어 있으며, 이는 실시간 결함 탐지 시스템 구현 시 가장 먼저 가속해야 할 정조준 영역임을 완벽히 실증합니다.
*   **Coreset 크기(메모리 뱅크)에 따른 런타임/메모리 비례 스케일링 확인**:
    *   학습 셋 크기가 가장 작은 `toothbrush`(60장)는 kNN Search 비중이 **75.1% (146.20 ms)**로 낮고 Peak Memory도 **223.84 MB**에 불과합니다.
    *   반면, 학습 셋 크기가 가장 거대한 `hazelnut`(391장)은 kNN Search 비중이 **94.7% (868.22 ms)**로 치솟고 Peak Memory 역시 **1405.80 MB (~1.4 GB)**를 점유합니다.
    *   이 계측 데이터는 Exact L2 kNN 탐색 지연 시간 및 메모리 뱅크 적재 메모리가 Coreset 메모리 뱅크의 크기에 따라 정확히 비례 팽창함을 실증합니다.
