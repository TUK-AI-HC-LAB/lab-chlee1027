# SimpleNet vs PatchCore — MVTec AD 15개 카테고리 직접 비교

> 작성: 2026-05-20
> method1: PatchCore (Roth 2022) — `method1_patchcore/markdown/baseline_full_table.md`
> method2: SimpleNet (Liu 2023) — `method2_simplenet/markdown/baseline_full_table.md`

## 1. 목적
동일 데이터셋(MVTec AD)·동일 백본(WideResNet-50, layer2+3)에서 재현한 PatchCore와 SimpleNet의 카테고리별 성능을 나란히 비교하여, 두 method의 강·약점이 어디서 갈리는지 파악한다.

## 2. 비교 조건

| 항목 | PatchCore (method1) | SimpleNet (method2) |
|---|---|---|
| 메커니즘 | Memory bank + NN 거리 | Feature Adaptor + Discriminator(GAN) |
| 학습 | 불필요 (memory bank만 구축) | 필요 (Adaptor + Discriminator) |
| 백본 / 레이어 | WRN-50 / layer2+3 | WRN-50 / layer2+3 |
| 입력 크기 | resize 256 / crop 224 | resize 329 / crop 288 |
| seed | 0 | 0 |

> **주의:** 입력 해상도가 다르다(PatchCore 224 vs SimpleNet 288). 따라서 본 비교는 "각 method를 논문 권장 설정으로 재현했을 때"의 비교이며, 입력 크기를 완전히 통제한 ablation은 아니다. 엄밀한 동일 조건 비교는 향후 입력 크기를 맞춘 추가 실험이 필요.

## 3. 카테고리별 비교 (재현값 기준)

I·P 모두 재현(Repro) 값. ΔI, ΔP = SimpleNet − PatchCore (양수면 SimpleNet 우위).

| Category | I-AUROC (PC) | I-AUROC (SN) | ΔI | P-AUROC (PC) | P-AUROC (SN) | ΔP |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| bottle | 1.000 | 1.000 | +0.000 | 0.985 | 0.980 | -0.005 |
| cable | 0.997 | 0.999 | +0.002 | 0.984 | 0.974 | -0.010 |
| capsule | 0.979 | 0.976 | -0.003 | 0.990 | 0.988 | -0.002 |
| carpet | 0.986 | 0.995 | +0.009 | 0.991 | 0.980 | -0.011 |
| grid | 0.979 | 0.998 | **+0.019** | 0.988 | 0.981 | -0.007 |
| hazelnut | 1.000 | 0.999 | -0.001 | 0.987 | 0.976 | -0.011 |
| leather | 1.000 | 1.000 | +0.000 | 0.993 | 0.992 | -0.001 |
| metal_nut | 0.999 | 1.000 | +0.001 | 0.983 | 0.986 | +0.003 |
| pill | 0.967 | 0.986 | **+0.019** | 0.978 | 0.984 | +0.006 |
| screw | 0.988 | 0.975 | **-0.013** | 0.995 | 0.988 | -0.007 |
| tile | 0.995 | 0.999 | +0.004 | 0.957 | 0.961 | +0.004 |
| toothbrush | 1.000 | 0.997 | -0.003 | 0.986 | 0.984 | -0.002 |
| transistor | 0.999 | 1.000 | +0.001 | 0.961 | 0.969 | +0.008 |
| wood | 0.991 | 1.000 | +0.009 | 0.951 | 0.940 | -0.011 |
| zipper | 0.995 | 1.000 | +0.005 | 0.989 | 0.980 | -0.009 |
| **Mean** | **0.992** | **0.995** | **+0.003** | **0.982** | **0.980** | **-0.002** |

**승패 요약**
- **I-AUROC (이미지 단위 탐지):** SimpleNet 9승 / PatchCore 4승 / 무승부 2
- **P-AUROC (픽셀 단위 위치추정):** PatchCore 11승 / SimpleNet 4승

## 4. 핵심 발견

### 4.1 Image-level은 SimpleNet, Pixel-level은 PatchCore
- **탐지(I-AUROC)**: SimpleNet이 평균 +0.003 우위. 특히 **텍스처 계열(grid +0.019, carpet +0.009, wood +0.009)** 에서 큰 폭으로 앞섬. 학습 기반으로 도메인에 적응한 Feature Adaptor가 텍스처 변화를 더 잘 잡는 것으로 보인다.
- **위치추정(P-AUROC)**: PatchCore가 15개 중 11개에서 우위. memory bank가 보존하는 **세밀한 공간 정보**가 픽셀 단위 정밀도에 유리한 것으로 해석된다. SimpleNet은 평균 -0.002.

### 4.2 PatchCore의 약점(pill·metal_nut)을 SimpleNet이 메움
- **pill:** PatchCore가 재현에서 가장 부진했던 카테고리(I 0.967). SimpleNet은 **I +0.019, P +0.006로 양쪽 모두 우위**. PatchCore의 "샘플링 역설"(method1 분석)에서 드러난 약점을, SimpleNet은 학습 기반 접근으로 보완.
- **metal_nut:** PatchCore의 P-AUROC가 논문 대비 낮았던(method1 -0.008) 카테고리. SimpleNet은 **P +0.003**로 앞서고 I는 1.000으로 동률 최고.
- → **PatchCore가 어려워한 곳에서 SimpleNet이 강하다**는 패턴. 두 method가 상보적임을 시사.

### 4.3 SimpleNet의 약점: screw
- **screw:** PatchCore가 I +0.013, P +0.007로 양쪽 우위. SimpleNet은 I-AUROC 0.975로 가장 부진. method2 분석에서 지적한 **Gaussian noise + Discriminator(GAN) 학습의 확률적 요소**가 작은 결함(나사산) 검출에서 불리하게 작용한 것으로 보인다.

## 5. 결론 및 다음
- 두 method는 **상보적**이다: 탐지 정확도(특히 텍스처)는 SimpleNet, 위치추정 정밀도는 PatchCore. PatchCore의 약점(pill·metal_nut)을 SimpleNet이 보완.
- 단, 입력 해상도 차이(224 vs 288)가 비교에 섞여 있으므로, **입력 크기를 통제한 추가 ablation**으로 검증 필요.
- method3(Reverse Distillation)을 같은 표에 추가하면 3-way 비교로 확장 가능 — RD는 복원 오차 기반이라 pixel-level에서 어떤 거동을 보일지 관심.

> 원자료: `method1_patchcore/markdown/baseline_full_table.md`, `method2_simplenet/markdown/baseline_full_table.md`
