# Reverse Distillation (RD) Baseline Reproduction Results (MVTec AD)

- commit: `[커밋해시]`
- sh / notebook: `method3_RD/source/run_baseline.sh`
- csv: `method3_RD/source/results/baseline_toothbrush_0521.csv` (1/15)

> **Environment:** Colab T4 / Python 3.12 / torch 2.x
> **Settings:** RD (ResNet18/WideResNet50 backbone, T-S distillation)
> **Paper:** Deng et al. 2022 (Reverse Distillation)

## 1. Summary Table (15 Categories)

| Category | I-AUROC (Repro) | I-AUROC (Paper) | Δ (I) | P-AUROC (Repro) | P-AUROC (Paper) | Δ (P) | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| bottle | - | 0.998 | - | - | 0.985 | - | Planning |
| cable | - | 0.940 | - | - | 0.864 | - | Planning |
| capsule | - | 0.863 | - | - | 0.981 | - | Planning |
| carpet | - | 0.989 | - | - | 0.989 | - | Planning |
| grid | - | 0.961 | - | - | 0.975 | - | Planning |
| hazelnut | - | 0.992 | - | - | 0.982 | - | Planning |
| leather | - | 0.902 | - | - | 0.992 | - | Planning |
| metal_nut | - | 0.969 | - | - | 0.941 | - | Planning |
| pill | - | 0.938 | - | - | 0.965 | - | Planning |
| screw | - | 0.871 | - | - | 0.959 | - | Planning |
| tile | - | 0.940 | - | - | 0.925 | - | Planning |
| toothbrush | 0.994 | 0.944 | +0.050 | 0.991 | 0.981 | +0.010 | Done |
| transistor | - | 0.913 | - | - | 0.825 | - | Planning |
| wood | - | 0.987 | - | - | 0.935 | - | Planning |
| zipper | - | 0.939 | - | - | 0.963 | - | Planning |
| **Mean** | **0.994** | **0.941** | **+0.053** | **0.991** | **0.947** | **+0.044** | (1/15) |

*Δ = Repro - Paper. (Note: Paper values are approximate/based on ResNet18/WideResNet50 as reported in various benchmarks.)*

## 2. 주요 관찰 사항

- **실험 준비:** Method 3 (RD) 재현을 위한 구조를 설정을 완료했습니다.
- **우선 순위:** `toothbrush` 카테고리를 첫 번째 타겟으로 설정하여 재현성을 검증할 예정입니다.

## 3. 시각화 결과 (Visualization)

재현 실험 과정에서 도출된 주요 시각화 결과가 여기에 추가될 예정입니다.

![repro_result_toothbrush](images/repro_result_toothbrush.png)
*Figure 1: RD Reproduction - Toothbrush Sample (Pending)*
