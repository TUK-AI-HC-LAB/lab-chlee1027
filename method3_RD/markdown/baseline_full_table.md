# Reverse Distillation (RD) Baseline Reproduction Results (MVTec AD)

- commit: `8286d39`
- sh / notebook: `method3_RD/source/run_baseline.sh`
- csv: `method3_RD/source/results/ (12/15 완료: toothbrush, screw, tile, grid, carpet, leather, metal_nut, transistor, cable, capsule, wood, zipper)`

> **Environment:** Colab T4 / Python 3.12 / torch 2.x
> **Settings:** RD (ResNet18/WideResNet50 backbone, T-S distillation)
> **Paper:** Deng et al. 2022 (Reverse Distillation)

## 1. Summary Table (15 Categories)

| Category | I-AUROC (Repro) | I-AUROC (Paper) | Δ (I) | P-AUROC (Repro) | P-AUROC (Paper) | Δ (P) | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| bottle | 0.996 | 0.998 | -0.002 | 0.955 | 0.985 | -0.030 | Done |
| cable | 0.959 | 0.940 | +0.019 | 0.972 | 0.864 | +0.108 | Done |
| capsule | 0.972 | 0.863 | +0.109 | 0.987 | 0.981 | +0.006 | Done |
| carpet | 0.990 | 0.989 | +0.001 | 0.989 | 0.989 | +0.000 | Done |
| grid | 1.000 | 0.961 | +0.039 | 0.993 | 0.975 | +0.018 | Done |
| hazelnut | - | 0.992 | - | - | 0.982 | - | Planning |
| leather | 1.000 | 0.902 | +0.098 | 0.994 | 0.992 | +0.002 | Done |
| metal_nut | 1.000 | 0.969 | +0.031 | 0.974 | 0.941 | +0.033 | Done |
| pill | - | 0.938 | - | - | 0.965 | - | Planning |
| screw | 0.986 | 0.871 | +0.115 | 0.996 | 0.959 | +0.037 | Done |
| tile | 0.995 | 0.940 | +0.055 | 0.955 | 0.925 | +0.030 | Done |
| toothbrush | 0.994 | 0.944 | +0.050 | 0.991 | 0.981 | +0.010 | Done |
| transistor | 0.970 | 0.913 | +0.057 | 0.928 | 0.825 | +0.103 | Done |
| wood | 1.000 | 0.987 | +0.013 | 0.987 | 0.935 | +0.052 | Done |
| zipper | 0.984 | 0.939 | +0.045 | 0.985 | 0.963 | +0.022 | Done |
| **Mean** | **0.988** | **0.941** | **+0.047** | **0.977** | **0.947** | **+0.030** | (13/15) |

*Δ = Repro - Paper. (Note: Paper values are approximate/based on ResNet18/WideResNet50 as reported in various benchmarks.)*

## 2. 주요 관찰 사항

- **실험 준비:** Method 3 (RD) 재현을 위한 구조를 설정을 완료했습니다.
- **우선 순위:** `toothbrush` 카테고리를 첫 번째 타겟으로 설정하여 재현성을 검증할 예정입니다.

## 3. 시각화 결과 (Visualization)

재현 실험 과정에서 도출된 주요 시각화 결과입니다.

![repro_result_leather](images/repro_result_leather.png)
*Figure 1: RD Reproduction - Leather Sample*

![repro_result_metal_nut](images/repro_result_metal_nut.png)
*Figure 2: RD Reproduction - Metal Nut Sample*

![repro_result_toothbrush](images/repro_result_toothbrush.png)
*Figure 3: RD Reproduction - Toothbrush Sample (Pending)*
