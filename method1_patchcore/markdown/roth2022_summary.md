# Roth et al. 2022 — Towards Total Recall in Industrial Anomaly Detection (PatchCore)

> Karsten Roth, Latha Pemula, Joaquin Zepeda, Bernhard Schölkopf, Thomas Brox, Peter Gehler. CVPR 2022.
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

## 본 재현과의 매칭 (PatchCore-10%, WRN-50)

| 카테고리 | 지표 | 재현 | 논문 |
|---|---|---|---|
| bottle | I-AUROC | 1.000 | 1.000 |
| bottle | P-AUROC | 0.985 | 0.986 |
| leather | I-AUROC | 1.000 | 1.000 |
| leather | P-AUROC | 0.993 | 0.990 |

→ ±0.005 이내. 자세한 분석: `method1_patchcore/markdown/baseline_analysis.md`

## 짚어둘 것 / 의문

- **coreset ratio**가 성능-속도 트레이드오프의 핵심. 1%로 줄여도 성능이 큰 폭 떨어지지 않는 이유는 greedy coreset이 분포의 외곽(=드문 정상 예시)을 잘 보존하기 때문 (논문 § 3.3).
- **단순 NN의 한계**: bank의 분포 편향이 그대로 드러남. 후속 연구들은 density 추정, distillation, reverse distillation 등으로 보완.
- **학습 없이도 SOTA** — task가 본질적으로 ImageNet feature space에서 잘 풀리는 문제임을 시사. 자연 이미지에 가까운 도메인(MVTec AD)에선 강하고, 의료·천체 같이 도메인 시프트가 큰 영역에선 다를 가능성.
- 이미지가 saturating(거의 1.000)되는 카테고리들은 method 비교에서 변별력이 약함 — ablation·후속 연구 비교는 어려운 카테고리(cable, transistor 등)에서 봐야 의미 있음.

## 다음

- coreset 비율 ablation (1%, 25%) — 직접 확인
- 백본 비교 (WRN-50 vs DINO ViT 등)
- MVTec AD 전체 카테고리(15개) baseline 풀세트 확보
- PatchCore 후속(예: PNI, EfficientAD) 1편 골라 다음 method 후보로 정하기
