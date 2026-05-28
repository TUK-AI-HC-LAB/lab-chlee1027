# Roth et al. 2022 — Towards Total Recall in Industrial Anomaly Detection (PatchCore)

## Paper Metadata

| 항목 | 내용 |
|---|---|
| 제목 | Towards Total Recall in Industrial Anomaly Detection |
| 저자 | Karsten Roth, Latha Pemula, Joaquin Zepeda, Bernhard Schölkopf, Thomas Brox, Peter Gehler |
| 학회/저널 | CVPR |
| 연도 | 2022 |
| 논문 링크 | [CVPR 2022 Open Access](https://openaccess.thecvf.com/content/CVPR2022/html/Roth_Towards_Total_Recall_in_Industrial_Anomaly_Detection_CVPR_2022_paper.html) |
| GitHub / 공식 코드 | [amazon-science/patchcore-inspection](https://github.com/amazon-science/patchcore-inspection) |
| 조사 이유 | 산업 제조 결함 탐지를 위한 대표적인 메모리 뱅크 및 coreset 샘플링 기반 baseline 알고리즘 분석 및 재현을 위함 |

> 원문 PDF: `method1_patchcore/paper/roth2022.pdf`

## 한 줄 요약

ImageNet 사전학습 백본의 **중간층 patch feature**를 정상 이미지에서 뽑아 **memory bank**에 저장하고, **coreset subsampling**으로 크기를 줄인 뒤, 테스트 이미지의 patch feature를 nearest-neighbor 거리로 채점한다. 학습 없이도 MVTec AD에서 SOTA.

## 문제 / 동기

- **Cold-start anomaly detection**: 정상 데이터만 있고 비정상은 거의 없는 산업 환경
- 기존 방법들의 한계
  - SPADE/PaDiM: 정상 분포 모델링 기반 — 적은 데이터에서 약하거나 추론 메모리·시간 비용 큼
  - 합성 결함 기반 방법: 실제 결함 분포와 어긋남
- 목표: **적은 정상 데이터로도 robust하고, 추론 비용은 낮은** 검출기

## 핵심 아이디어 3가지

### 1. Locally-aware patch features

- ImageNet pretrain 백본의 중간층(예: WRN-50의 layer2 + layer3) feature map 사용
- 각 위치 feature를 **이웃 평균(adaptive avg pooling)** 으로 묶어 patch-level descriptor 생성
- **얕은 층은 너무 generic, 깊은 층은 ImageNet 분류용 추상 feature** 라 둘 다 부적합. mid-level이 핵심

### 2. Memory bank + coreset subsampling

- 모든 정상 patch feature를 모아 memory bank 구성 (수만~수십만 개)
- **greedy coreset**으로 서브샘플링 (논문에선 1%, 10%, 25% 비교)
- coreset은 분포의 **외곽**을 잘 보존 → 작은 비율로도 성능 거의 유지
- 본 재현은 10% (논문에서 "PatchCore-10%")

### 3. Nearest-neighbor 채점

- 테스트 patch feature 각각에 대해 memory bank의 NN 거리 → patch-level anomaly score
- 이미지 점수 = max patch score에 reweighting (이웃 NN 거리 비교 기반)

## 주요 결과 (논문 Table 1·2 발췌)

- MVTec AD 평균 Image-AUROC: **99.1%** (PatchCore-1%) → **99.6%** (PatchCore-100%)
- 다수 카테고리에서 100% Image-AUROC (bottle, leather, pill, screw 등)
- Pixel-AUROC도 모든 비교군 대비 상위
- VisA, MVTec 3D-AD 등 다른 anomaly detection 데이터셋에서도 강함
- 학습이 필요 없어 백본만 갈아끼면 즉시 적용 가능

## 본 재현과의 매칭 (PatchCore-10%, WRN-50, 15/15 완료)

| 지표 | 재현 평균 (15개) | 논문 평균 | Δ |
|---|---|---|---|
| I-AUROC | **0.992** | 0.991 | +0.001 |
| P-AUROC | **0.982** | 0.981 | +0.001 |

- 15개 전 카테고리 모두 재현 완료 (2026-05-06 ~ 05-11)
- bottle·hazelnut·leather·toothbrush에서 I-AUROC 1.000 달성
- `pill`(-0.011), `metal_nut`(P -0.008) 하락 원인 분석 및 검증 실험 완결

→ 상세 분석: `method1_patchcore/markdown/baseline_analysis.md`
→ 원인 분석: `method1_patchcore/markdown/repro_failure_analysis.md`
→ 카테고리별 상세: `method1_patchcore/markdown/baseline_full_table.md`

