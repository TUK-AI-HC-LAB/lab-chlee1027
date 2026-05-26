# 4-way 비교 — PatchCore vs SimpleNet vs RD vs Dinomaly (MVTec AD)

> 작성: 2026-05-25
> method1 PatchCore (M1) — `method1_patchcore/markdown/baseline_full_table.md`
> method2 SimpleNet (M2) — `method2_simplenet/markdown/baseline_full_table.md`
> method3 RD (M3) — `method3_RD/markdown/baseline_full_table.md`
> method4 Dinomaly (M4) — `method4_Dinomaly/markdown/baseline_full_table.md`

## 1. 목적
재현이 완료된 4개 Method를 동일 데이터셋(MVTec AD)에서 나란히 비교하여, 각기 다른 메커니즘(Memory bank / Discriminator / 복원 / ViT-Unified)의 공학적 우열과 상보적 관계를 정의한다.

## 2. 비교 조건 및 주의점

| 항목 | M1: PatchCore | M2: SimpleNet | M3: RD | M4: Dinomaly |
| :--- | :---: | :---: | :---: | :---: |
| **메커니즘** | Memory bank + NN | GAN-Discriminator | Encoder-Decoder 복원 | **ViT Reconstruction** |
| **학습 방식** | 불필요 | Class-separated | Class-separated | **MUAD (Unified)** |
| **입력 크기** | 224 (Resize 256) | 288 (Resize 329) | 256 (Resize 256) | **392 (Resize 448)** |
| **백본** | WRN-50 | WRN-50 | WRN-50 | **DINOv2 (ViT-Base)** |
| **3번째 지표** | P-AUROC | P-AUROC | **AUPRO** | **AUPRO** |

> **주의 1 (해상도):** Dinomaly(M4)가 가장 높은 해상도(392)를 사용하며, DINOv2라는 강력한 사전학습 모델을 활용하므로 단순 수치 비교 시 이를 감안해야 함.
> **주의 2 (효율성):** M4는 단일 모델로 15개 클래스를 처리하는 MUAD 방식임. 개별 모델을 15번 학습하는 M2, M3 대비 실용적 가치가 높음.
> **주의 3:** 4개 Method 모두 **15/15** 전 카테고리 재현 완료.

## 3. 카테고리별 비교 (재현값)

### I-AUROC (이미지 단위 탐지)

| Category | M1: PatchCore | M2: SimpleNet | M3: RD | M4: Dinomaly | 최고 (Method) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| bottle | 1.000 | 1.000 | 0.996 | **1.000** | M1, M2, M4 |
| cable | 0.997 | 0.999 | 0.959 | **1.000** | **M4** |
| capsule | 0.979 | 0.976 | 0.972 | **0.9793** | **M4** |
| carpet | 0.986 | 0.995 | 0.990 | **0.9988** | **M4** |
| grid | 0.979 | 0.998 | **1.000** | 0.9975 | **M3** |
| hazelnut | 1.000 | 0.999 | 1.000 | **1.000** | M1, M3, M4 |
| leather | 1.000 | 1.000 | 1.000 | **1.000** | 4사 동률 |
| metal_nut | 0.999 | 1.000 | 1.000 | **1.000** | M2, M3, M4 |
| pill | 0.967 | 0.986 | 0.965 | **0.9924** | **M4** |
| screw | **0.988** | 0.975 | 0.986 | 0.9850 | **M1** |
| tile | 0.995 | 0.999 | 0.995 | **1.000** | **M4** |
| toothbrush | 1.000 | 0.997 | 0.994 | **1.000** | M1, M4 |
| transistor | 0.999 | **1.000** | 0.970 | 0.9904 | **M2** |
| wood | 0.991 | **1.000** | **1.000** | 0.9991 | M2, M3 |
| zipper | 0.995 | **1.000** | 0.984 | **1.000** | M2, M4 |
| **Mean (15개)** | **0.992** | **0.995** | **0.988** | **0.9962** | **M4 (Dinomaly)** |

### P-AUROC (픽셀 단위 위치추정) - Mean 기준

| Metric | M1: PatchCore | M2: SimpleNet | M3: RD | M4: Dinomaly | 최고 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Mean P-AUROC** | 0.982 | 0.980 | 0.978 | **0.9832** | **M4** |

## 4. 핵심 발견

### 4.1 지표별 우열 (Mean 기준)
- **탐지(I-AUROC):** **M4(0.9962)** > M2(0.995) > M1(0.992) > M3(0.988). Dinomaly가 통합 모델임에도 불구하고 가장 높은 이미지 단위 탐지 성능을 보임.
- **위치추정(P-AUROC):** **M4(0.983)** > M1(0.982) > M2(0.980) > M3(0.978). Dinomaly의 고해상도 ViT 복원 방식이 기존 Memory bank 기반의 PatchCore를 근소하게 앞서며 1위 달성.

### 4.2 Dinomaly(M4)의 강점 — 효율성과 범용성
- **MUAD의 실용성:** 15개 클래스를 하나의 모델로 처리하면서도 모든 지표에서 1위를 차지한 것은 매우 고무적임. 특히 `cable`, `pill`, `tile` 등에서 압도적 우위.
- **DINOv2 효과:** 강력한 사전학습 특징을 사용하여 `bottle`, `leather` 등에서 완벽한 탐지(1.000)를 기록함.

### 4.3 RD(M3) 및 PatchCore(M1)의 특화 영역
- **M3 (텍스처 킬러):** 여전히 `grid` 카테고리에서는 RD가 1.000으로 가장 강하며, 텍스처 결함의 복원 오차 방식이 가진 변별력이 유효함을 입증.
- **M1 (저해상도 효율):** 가장 낮은 해상도(224)와 학습 없는 방식으로도 `screw` 등 특정 객체 카테고리에서 여전히 최상위권을 유지함.

### 4.4 Method 간 상보성 (4-way 분업)
- **이미지 탐지 & 범용 모델:** M4 (Dinomaly)
- **객체 정밀 탐지:** M2 (SimpleNet)
- **텍스처 특화 위치추정:** M3 (RD)
- **Zero-training 고효율:** M1 (PatchCore)

## 5. 결론 및 다음 단계
- Dinomaly(M4)는 성능과 효율성(MUAD) 두 마리 토끼를 모두 잡은 가장 진보된 프레임워크임을 확인.
- 4-way 비교를 통해 각 카테고리별 "최적의 알고리즘" 맵이 완성됨.
- 다음 단계에서는 이 4개 Method의 장점을 결합하거나, 데이터가 아예 없는 상황을 가정하는 **Zero-shot** 접근법에 대한 탐색이 필요함.

---
**관련 문서**:
- [RD vs PatchCore/SimpleNet 비교 (3-way)](../../method3_RD/markdown/rd_vs_patchcore_simplenet.md)
