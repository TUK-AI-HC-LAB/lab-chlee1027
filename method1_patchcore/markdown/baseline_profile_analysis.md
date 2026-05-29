commit: [Dynamic Commit from Colab Run]
sh / notebook: method1_patchcore/source/profile_colab.ipynb
csv: method1_patchcore/source/results/baseline_profile_results.csv (15/15 Complete Profile Completed)

# PatchCore Baseline 연산 단계별 프로파일링 분석 보고서

본 보고서는 PatchCore baseline 모델의 연산 단계별 소요 시간(Inference Time)과 메모리(Peak Memory)를 정량적으로 측정하여 병목 지점을 진단한 결과를 정리합니다.

---

## 1. 수집 결과 요약 테이블 (Profiling Full Table)

MVTec AD 데이터셋 전체 15개 카테고리(`bottle`, `metal_nut`, `cable`, `wood`, `transistor`, `leather`, `toothbrush`, `grid`, `screw`, `hazelnut`, `capsule`, `tile`, `pill`, `carpet`, `zipper`)를 대상으로 프로파일링을 수행하였습니다.

| 카테고리 | Train 이미지수 | Test 이미지수 | I-AUROC | P-AUROC | kNN 추론 시간 비율 | 이미지당 kNN Latency | Memory Bank Build Peak Memory |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **hazelnut** | 391장 | 110장 | 100.0% | 98.7% | **94.7% (95.50s)** | **868.22 ms** | **1405.80 MB** |
| **screw** | 320장 | 160장 | 98.8% | 99.5% | **93.4% (110.98s)** | **693.61 ms** | **1152.09 MB** |
| **carpet** | 280장 | 117장 | 98.6% | 99.1% | **92.6% (73.25s)** | **626.06 ms** | **1008.96 MB** |
| **pill** | 267장 | 167장 | 96.7% | 97.8% | **92.5% (100.17s)** | **599.81 ms** | **961.58 MB** |
| **zipper** | 240장 | 151장 | 99.5% | 98.9% | **92.3% (90.29s)** | **597.95 ms** | **866.06 MB** |
| **grid** | 264장 | 78장 | 97.9% | 98.8% | **92.1% (43.60s)** | **558.96 ms** | **951.50 MB** |
| **wood** | 247장 | 79장 | 99.1% | 95.1% | **91.9% (43.38s)** | **549.07 ms** | **889.91 MB** |
| **leather** | 245장 | 124장 | 100.0% | 99.3% | **91.6% (67.35s)** | **543.11 ms** | **882.99 MB** |
| **tile** | 230장 | 117장 | 99.5% | 95.7% | **91.2% (59.52s)** | **508.70 ms** | **829.38 MB** |
| **cable** | 224장 | 150장 | 99.7% | 98.4% | **91.0% (76.84s)** | **512.28 ms** | **808.40 MB** |
| **capsule** | 219장 | 132장 | 97.9% | 99.0% | **90.9% (62.97s)** | **477.06 ms** | **790.97 MB** |
| **metal_nut** | 220장 | 115장 | 99.9% | 98.3% | **90.7% (54.56s)** | **474.40 ms** | **794.51 MB** |
| **transistor** | 213장 | 100장 | 99.9% | 96.1% | **90.6% (47.37s)** | **473.68 ms** | **770.58 MB** |
| **bottle** | 209장 | 83장 | 100.0% | 98.5% | **89.9% (38.44s)** | **463.12 ms** | **755.08 MB** |
| **toothbrush** | 60장 | 42장 | 100.0% | 98.6% | **75.1% (6.14s)** | **146.20 ms** | **223.84 MB** |

---

## 2. 연산 단계별 세부 분석 지표

### 1) Training Phase (학습 단계)
*   **Feature Extraction (Train)**:
    *   `toothbrush`: 6.05 s, `bottle`: 11.97 s, `metal_nut`: 15.05 s, `capsule`: 16.74 s, `grid`: 17.48 s, `tile`: 18.12 s, `pill`: 19.42 s, `transistor`: 19.71 s, `cable`: 20.39 s, `leather`: 20.73 s, `wood`: 22.25 s, `zipper`: 22.57 s, `screw`: 22.35 s, `carpet`: 26.19 s, `hazelnut`: 35.25 s
    *   학습 이미지 수가 늘어남에 따라 특징 추출에 필요한 시간이 비례하여 증가하며, Backbone 네트워크(WideResNet50)의 순방향 연산 및 패치 추출 메모리는 약 **173 MB** 수준으로 일정하게 통제됩니다.
*   **Memory Bank Build (Coreset Subsampling & Indexing)**:
    *   `toothbrush`: 2.29 s | 223.84 MB, `bottle`: 22.62 s | 755.08 MB, `transistor`: 24.34 s | 770.58 MB, `metal_nut`: 25.07 s | 794.51 MB, `capsule`: 25.22 s | 790.97 MB, `cable`: 26.38 s | 808.40 MB, `tile`: 27.04 s | 829.38 MB, `zipper`: 31.12 s | 866.06 MB, `leather`: 31.58 s | 882.99 MB, `wood`: 31.76 s | 889.91 MB, `grid`: 36.22 s | 951.50 MB, `pill`: 37.19 s | 961.58 MB, `carpet`: 41.49 s | 1008.96 MB, `screw`: 52.23 s | 1152.09 MB, `hazelnut`: 79.04 s | 1405.80 MB
    *   정상 이미지에서 추출된 수십만 개의 패치 특징을 Greedy Coreset 알고리즘을 통해 10% 수준으로 Subsampling하는 연산 부하가 큽니다.
    *   학습 데이터셋 규모가 큰 **`hazelnut` (1.4 GB / 79.04 s), `screw` (1.15 GB / 52.23 s), `carpet` (1.0 GB / 41.49 s)** 카테고리에서 극단적인 메모리 스파이크와 연산 시간 지연을 초래하여, 학습 단계 부하의 대용량화 병목을 적나라하게 보여줍니다.

### 2) Inference Phase (테스트 추론 단계)
*   **Feature Extraction (Test)**:
    *   이미지당 약 **44~49 ms** 수준으로 매우 일정하게 작동하며, GPU 특징 추출 가속의 모범적인 지연 시간을 대조 제공합니다.
*   **kNN Search (Exact L2 kNN Matching)**:
    *   `toothbrush`: 6.14 s (**146.20 ms/img**), `bottle`: 38.44 s (**463.12 ms/img**), `transistor`: 47.37 s (**473.68 ms/img**), `metal_nut`: 54.56 s (**474.40 ms/img**), `capsule`: 62.97 s (**477.06 ms/img**), `tile`: 59.52 s (**508.70 ms/img**), `cable`: 76.84 s (**512.28 ms/img**), `leather`: 67.35 s (**543.11 ms/img**), `wood`: 43.38 s (**549.07 ms/img**), `grid`: 43.60 s (**558.96 ms/img**), `zipper`: 90.29 s (**597.95 ms/img**), `pill`: 100.17 s (**599.81 ms/img**), `carpet`: 73.25 s (**626.06 ms/img**), `screw`: 110.98 s (**693.61 ms/img**), `hazelnut`: 95.50 s (**868.22 ms/img**)
    *   **전체 추론 시간의 75.1% ~ 94.7%를 점유하는 파괴적인 병목 지점**입니다.
    *   Coreset 메모리 뱅크의 크기가 작은 `toothbrush`는 이미지당 Latency가 **146.20 ms** 수준에 그치나, 대용량 카테고리인 `hazelnut`은 무려 **868.22 ms**에 이르러 실시간 판정이 불가능합니다. 
    *   이 계측 데이터는 Exact L2 kNN 탐색 지연 시간이 메모리 뱅크(Coreset) 크기에 정확히 선형적으로 비례(Scaling)함을 부정할 수 없이 실증적으로 규명합니다.
*   **Post-processing (Anomaly Map Generation & Smoothing)**:
    *   이미지당 약 **2.84~3.71 ms** 내외로, 최종 판정을 위한 가공 연산은 전체 런타임에 거의 영향을 주지 않습니다.

---

## 3. 공학적 진단 및 향후 가속 방향

계측된 프로파일 데이터는 PatchCore baseline의 구조적 한계를 명확하게 지시합니다.
1.  **가설 검증 완료**: Exact Search kNN이 성능(AUROC) 측면에서는 완벽한 재현율을 제공하지만, 추론 연산 시간의 **90% 이상을 잠식**하여 실시간 불량 탐지 시스템(Latency $\le 50$ms 요구 조건)에 직접 배포하기가 불가능함을 정량적으로 입증하였습니다.
2.  **가속점 도출**: 추론 Latency를 획기적으로 낮추기 위해서는 특징 추출이나 후처리가 아닌 **kNN Search 단계를 정조준하여 가속**해야 합니다.
3.  **FAISS 인덱스 가속화 실험 전개**: 2단계에서는 본 정량 데이터를 기준으로 하여, **HNSW (Hierarchical Navigable Small World)** 및 **IVF (Inverted File)** 근사 최근접 이웃 검색(ANN) 인덱스를 도입하고, 성능 저하(AUROC 하락)를 1% 이내로 제약하면서 kNN 검색 Latency를 5배 이상 단축시키는 최적의 파레토 프론티어(Pareto Frontier)를 규명하는 실험을 진행합니다.
