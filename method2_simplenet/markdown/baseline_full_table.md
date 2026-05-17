# SimpleNet Baseline Reproduction Results (MVTec AD)

- commit: `486146d`
- sh / notebook: `method2_simplenet/source/simplenet_colab.ipynb`
- csv: `method2_simplenet/source/results/baseline_toothbrush.csv` (15 categories planned)

> **Environment:** Colab T4 / Python 3.12 / torch 2.10.0+cu128
> **Settings:** SimpleNet (WideResNet50, layers 2+3, patchsize 3, meta_epochs 40, gan_epochs 4)
> **Paper:** Liu et al. 2023 (SimpleNet)

## 1. Summary Table (15 Categories)

| Category | I-AUROC (Repro) | I-AUROC (Paper) | Δ (I) | P-AUROC (Repro) | P-AUROC (Paper) | Δ (P) | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| bottle | - | 1.000 | - | - | 0.982 | - | Planning |
| cable | - | 0.995 | - | - | 0.985 | - | Planning |
| capsule | - | 0.985 | - | - | 0.990 | - | Planning |
| carpet | - | 0.992 | - | - | 0.990 | - | Planning |
| grid | - | 0.984 | - | - | 0.983 | - | Planning |
| hazelnut | - | 0.999 | - | - | 0.988 | - | Planning |
| leather | - | 1.000 | - | - | 0.993 | - | Planning |
| metal_nut | - | 1.000 | - | - | 0.981 | - | Planning |
| pill | - | 0.987 | - | - | 0.975 | - | Planning |
| screw | - | 0.992 | - | - | 0.996 | - | Planning |
| tile | - | 0.999 | - | - | 0.966 | - | Planning |
| toothbrush | 1.000 | 0.991 | +0.009 | 0.985 | 0.984 | +0.001 | Done |
| transistor | - | 1.000 | - | - | 0.977 | - | Planning |
| wood | - | 0.992 | - | - | 0.949 | - | Planning |
| zipper | - | 0.998 | - | - | 0.991 | - | Planning |
| **Mean** | - | **0.996** | - | - | **0.981** | - | (1/15) |

*Δ = Repro - Paper. (Paper values are based on WRN50 backbone results from the original paper)*

## 2. 주요 관찰 사항 (Summary)

- **1차 재현 (2026-05-17):** `toothbrush` 카테고리 재현 완료. I-AUROC 1.000, P-AUROC 0.985로 논문 수치(각각 0.991, 0.984)를 상회하거나 동등한 수준 기록.
- **시각화 패치:** `main.py` 내의 테스트 로직 버그를 수정하여 히트맵(Segmentation) 이미지가 정상적으로 저장되도록 조치함.
- **향후 계획:** 나머지 14개 카테고리에 대해 순차적으로 실험을 진행하여 PatchCore와의 성능 격차를 분석할 예정.
