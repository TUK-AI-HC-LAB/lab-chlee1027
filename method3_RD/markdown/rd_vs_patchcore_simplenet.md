# 3-way 비교 — PatchCore vs SimpleNet vs Reverse Distillation (MVTec AD)

> 작성: 2026-05-21
> method1 PatchCore (Roth 2022) — `method1_patchcore/markdown/baseline_full_table.md`
> method2 SimpleNet (Liu 2023) — `method2_simplenet/markdown/baseline_full_table.md`
> method3 RD (Deng 2022) — `method3_RD/markdown/baseline_full_table.md`

## 1. 목적
동일 데이터셋(MVTec AD)에서 재현한 세 method를 카테고리별로 나란히 비교하여, 메커니즘이 다른 세 접근(memory bank / GAN-discriminator / encoder-decoder 복원)의 강·약점이 어디서 갈리는지 파악한다.

## 2. 비교 조건 및 주의점

| 항목 | PatchCore | SimpleNet | Reverse Distillation |
|---|---|---|---|
| 메커니즘 | Memory bank + NN 거리 | Feature Adaptor + Discriminator(GAN) | Encoder-Decoder 복원 오차 |
| 학습 | 불필요 | 필요 | 필요 |
| 백본 | WRN-50 | WRN-50 | WRN-50 |
| 입력 크기 | 256/224 | 329/288 | 256 |
| 3번째 지표 | anomaly pixel AUROC | anomaly pixel AUROC | **AUPRO** (Per-Region Overlap) |

> **주의 1:** 입력 해상도와 학습 설정이 method마다 달라, 본 비교는 "각 method를 권장 설정으로 재현했을 때"의 비교이지 완전 통제 ablation은 아니다.
> **주의 2:** 세 method의 3번째 픽셀 지표가 다르다(RD는 AUPRO). 따라서 직접 비교는 **I-AUROC**와 **Full P-AUROC** 두 지표로 한정한다.
> **주의 3:** RD는 현재 **14/15** 진행 (hazelnut 미완) — 해당 칸은 공란.

## 3. 카테고리별 비교 (재현값)

### I-AUROC (이미지 단위 탐지)

| Category | PatchCore | SimpleNet | RD | 최고 |
| :--- | :---: | :---: | :---: | :---: |
| bottle | 1.000 | 1.000 | 0.996 | PC=SN |
| cable | 0.997 | 0.999 | 0.959 | SN |
| capsule | 0.979 | 0.976 | 0.972 | PC |
| carpet | 0.986 | 0.995 | 0.990 | SN |
| grid | 0.979 | 0.998 | 1.000 | RD |
| hazelnut | 1.000 | 0.999 | – | PC |
| leather | 1.000 | 1.000 | 1.000 | 3사 동률 |
| metal_nut | 0.999 | 1.000 | 1.000 | SN=RD |
| pill | 0.967 | 0.986 | 0.965 | SN |
| screw | 0.988 | 0.975 | 0.986 | PC |
| tile | 0.995 | 0.999 | 0.995 | SN |
| toothbrush | 1.000 | 0.997 | 0.994 | PC |
| transistor | 0.999 | 1.000 | 0.970 | SN |
| wood | 0.991 | 1.000 | 1.000 | SN=RD |
| zipper | 0.995 | 1.000 | 0.984 | SN |
| **평균(전체)** | **0.992** | **0.995** | **0.987** (14개) | |
| **평균(공통 14개)** | **0.991** | **0.995** | **0.987** | **SN** |

### Full P-AUROC (픽셀 단위 위치추정)

| Category | PatchCore | SimpleNet | RD | 최고 |
| :--- | :---: | :---: | :---: | :---: |
| bottle | 0.985 | 0.980 | 0.955 | PC |
| cable | 0.984 | 0.974 | 0.972 | PC |
| capsule | 0.990 | 0.988 | 0.987 | PC |
| carpet | 0.991 | 0.980 | 0.989 | PC |
| grid | 0.988 | 0.981 | 0.993 | RD |
| hazelnut | 0.987 | 0.976 | – | PC |
| leather | 0.993 | 0.992 | 0.994 | RD |
| metal_nut | 0.983 | 0.986 | 0.974 | SN |
| pill | 0.978 | 0.984 | 0.982 | SN |
| screw | 0.995 | 0.988 | 0.996 | RD |
| tile | 0.957 | 0.961 | 0.955 | SN |
| toothbrush | 0.986 | 0.984 | 0.991 | RD |
| transistor | 0.961 | 0.969 | 0.928 | SN |
| wood | 0.951 | 0.940 | 0.987 | **RD** |
| zipper | 0.989 | 0.980 | 0.985 | PC |
| **평균(전체)** | **0.982** | **0.980** | **0.978** (14개) | |
| **평균(공통 14개)** | **0.981** | **0.978** | **0.978** | **PC** |

## 4. 핵심 발견

### 4.1 지표별 우열 (공통 14개 카테고리 기준)
- **탐지(I-AUROC):** SimpleNet(0.995) > PatchCore(0.991) > RD(0.987). 학습 기반 두 method가 이미지 단위 탐지에서 강하고, RD가 근소하게 뒤짐.
- **위치추정(Full P-AUROC):** PatchCore(0.981) > SimpleNet(0.978) = RD(0.978). memory bank의 세밀한 공간 정보가 픽셀 정밀도에서 여전히 1위. SimpleNet과 RD는 평균은 같지만 **카테고리별 강점이 정반대**(아래 4.2~4.3).

### 4.2 RD의 강점 — 텍스처 픽셀 정밀도
- **wood:** RD P-AUROC **0.987** vs PatchCore 0.951 / SimpleNet 0.940 — **RD가 압도적**(+0.036). encoder-decoder 복원 방식이 나뭇결 같은 텍스처 결함의 픽셀 경계를 더 잘 잡는 것으로 보인다.
- **screw(P 0.996), leather(P 0.994), grid(P 0.993), toothbrush(P 0.991):** RD가 픽셀 최고. 복원 오차 기반이 미세 구조 위치추정에 유리.

### 4.3 RD의 약점 — transistor·cable·bottle(픽셀)
- **transistor:** RD I 0.970 / P 0.928 — 세 method 중 양쪽 모두 최저. 부품 위치·배선 변화처럼 "정상 패턴이 다양한" 카테고리에서 복원 모델이 약함.
- **cable:** RD I 0.959 — 최저. 비슷한 이유로 추정.
- **bottle(픽셀):** RD P 0.955 vs PatchCore 0.985 / SimpleNet 0.980 — 이미지 탐지는 0.996로 높지만 픽셀 위치추정이 두 method 대비 -0.03 낮음.

### 4.4 method 간 상보성
- **PatchCore가 약했던 pill·metal_nut:** metal_nut은 SimpleNet·RD 모두 I-AUROC 1.000 달성. pill은 이미지 탐지에서 SimpleNet(0.986)이 PatchCore(0.967)를 크게 보완하고, 픽셀에서는 RD(0.982)·SimpleNet(0.984)이 PatchCore(0.978)를 앞섬.
- **세 method의 분업 구도:** 이미지 탐지=SimpleNet, 범용 픽셀 정밀도=PatchCore, 텍스처 픽셀 정밀도=RD. 단일 method가 모든 카테고리를 지배하지 않음.

## 5. 결론 및 다음
- 세 접근은 **상보적**이며, 카테고리 특성(객체 vs 텍스처)·평가 축(이미지 vs 픽셀)에 따라 우열이 갈린다.
- **남은 작업:** RD의 hazelnut 완료 후 15/15 기준으로 평균 재계산.
- 입력 해상도·학습 설정 차이가 비교에 섞여 있으므로, 동일 입력 크기로 맞춘 통제 실험이 후속 과제.

> 원자료: 세 method의 `baseline_full_table.md` / `source/results/*.csv`
> 2-way 상세(PatchCore↔SimpleNet): `method2_simplenet/markdown/simplenet_vs_patchcore.md`
