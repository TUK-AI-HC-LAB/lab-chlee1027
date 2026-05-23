# SimpleNet screw·capsule 편차 원인 분석 및 구조적 가설 검증 보고서

## 1. 개요 및 문제 정의
SimpleNet의 MVTec AD 재현 과정에서 `screw` (I-AUROC -0.017) 및 `capsule` (-0.009) 카테고리의 성능이 논문 대비 유의미하게 하락하였습니다. 기존에는 이를 "GAN 학습의 확률적 요소"로만 해석하였으나, 동일 환경에서 PatchCore가 `screw`에서 우위(I-AUROC +0.013)를 점한 것과 대조하면, 이는 단순 오차가 아닌 **SimpleNet의 구조적 한계**일 가능성이 높습니다.

본 보고서는 이를 규명하기 위한 구조적 가설을 설정하고, 이를 검증하기 위한 실험 로드맵을 제시합니다.

---

## 2. 구조적 가설: Gaussian Noise와 Discriminator의 트레이드오프

### 2.1. 가설 설정
SimpleNet은 정상 특징에 **Gaussian Noise**를 주입하여 가상 이상치(synthetic anomalies)를 생성하고, 이를 **Discriminator**가 구분하도록 학습합니다. 이때 다음과 같은 구조적 약점이 발생할 수 있습니다:
- **Noise Masking:** 주입되는 Gaussian noise ($\sigma$)의 크기가 실제 `screw`의 나사산 결함과 같은 미세한(fine-grained) 특징 변화보다 클 경우, 실제 결함이 노이즈에 묻혀 Discriminator가 학습하지 못할 수 있습니다.
- **Discriminator Overfitting:** Discriminator가 특정 epoch에서 가상 노이즈 패턴에 과적합될 경우, 실제 데이터의 미세한 변위(small defects)를 포착하는 일반화 능력이 저하될 수 있습니다.

### 2.2. PatchCore와의 비교 관점
- **PatchCore (Memory Bank):** 특징점 간의 거리를 직접 비교하므로 미세한 변위가 메모리 뱅크에 존재하지 않으면 즉시 이상치로 간주합니다. (Small defect에 강함)
- **SimpleNet (Discriminator):** 학습을 통해 '경계'를 결정하므로, 경계 설정에 사용된 노이즈의 특성에 따라 미세 결함이 '정상' 영역 내로 포함될 위험이 있습니다.

---

## 3. 실험 로드맵 (Proposed Experiments)

단순 재현 잡음(Reproduction Noise)과 구조적 약점(Structural Weakness)을 분리하기 위해 아래 실험을 제안합니다.

### 3.1. 실험 A: 확률적 요소의 정량화 (Multi-seed Run)
- **내용:** 동일 설정(Seed 1, 2, 3)으로 3회 반복 실행.
- **목적:** 성능 편차의 표준편차를 계산하여, 현재의 하락이 단순 "운"(stochasticity)인지, 아니면 반복적으로 발생하는 하락인지 확인.

### 3.2. 실험 B: 노이즈 민감도 분석 ($\sigma$ Ablation)
- **내용:** `noise_std` 값을 기존 0.015에서 0.010, 0.005 등으로 하향 조정.
- **목적:** 노이즈 강도를 낮추었을 때 `screw`의 미세 결함 탐지력이 복원되는지 확인. (노이즈가 결함을 마스킹한다는 가설 검증)

### 3.3. 실험 C: 학습 성숙도 분석 (Discriminator Epoch Ablation)
- **내용:** `gan_epochs`를 기존 4에서 2, 6 등으로 조절.
- **목적:** 특정 학습 시점에서 `screw` 성능이 피크를 치고 하락(과적합)하는지, 혹은 학습 부족인지 확인.

---

## 4. 기대 효과 및 활용 방안
- **Method 비교 근거 격상:** 단순한 "재현 실패" 보고를 넘어, "SimpleNet은 텍스처에 강하나 미세 구조 결함(screw)에는 취약할 수 있다"는 공학적 비교 근거로 활용.
- **최적화 가이드 제공:** 카테고리별 특성(Small vs Large defect)에 따른 `noise_std` 및 `epoch` 최적화 가이드라인 제시.

---
**작성일:** 2026-05-23
**관련 문서:** 
- [SimpleNet vs PatchCore 비교](simplenet_vs_patchcore.md)
- [PatchCore 편차 분석 사례](../../method1_patchcore/markdown/repro_failure_analysis.md)
