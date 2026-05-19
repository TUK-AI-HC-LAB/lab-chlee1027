# SimpleNet Baseline Reproduction Results (MVTec AD)

- commit: `486146d`
- sh / notebook: `method2_simplenet/source/simplenet_colab.ipynb`
- csv: `method2_simplenet/source/results/baseline_grid.csv` (15 categories planned)

> **Environment:** Colab T4 / Python 3.12 / torch 2.10.0+cu128
> **Settings:** SimpleNet (WideResNet50, layers 2+3, patchsize 3, meta_epochs 40, gan_epochs 4)
> **Parameters:** batchsize 8, resize 329, imagesize 288 (Paper matching)
> **Paper:** Liu et al. 2023 (SimpleNet)

## 1. Summary Table (15 Categories)

| Category | I-AUROC (Repro) | I-AUROC (Paper) | Δ (I) | P-AUROC (Repro) | P-AUROC (Paper) | Δ (P) | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| bottle | 1.000 | 1.000 | +0.000 | 0.980 | 0.982 | -0.002 | Done |
| cable | 0.999 | 0.995 | +0.004 | 0.974 | 0.985 | -0.011 | Done |
| capsule | - | 0.985 | - | - | 0.990 | - | Planning |
| carpet | - | 0.992 | - | - | 0.990 | - | Planning |
| grid | 0.998 | 0.984 | +0.014 | 0.981 | 0.983 | -0.002 | Done |
| hazelnut | 0.999 | 0.999 | +0.000 | 0.976 | 0.988 | -0.012 | Done |
| leather | 1.000 | 1.000 | +0.000 | 0.992 | 0.993 | -0.001 | Done |
| metal_nut | 1.000 | 1.000 | +0.000 | 0.986 | 0.981 | +0.005 | Done |
| pill | 0.986 | 0.987 | -0.001 | 0.984 | 0.975 | +0.009 | Done |
| screw | - | 0.992 | - | - | 0.996 | - | Planning |
| tile | 0.999 | 0.999 | +0.000 | 0.961 | 0.966 | -0.005 | Done |
| toothbrush | 0.997 | 0.991 | +0.006 | 0.984 | 0.984 | +0.000 | Done |
| transistor | 1.000 | 1.000 | +0.000 | 0.969 | 0.977 | -0.008 | Done |
| wood | 1.000 | 0.992 | +0.008 | 0.940 | 0.949 | -0.009 | Done |
| zipper | - | 0.998 | - | - | 0.991 | - | Planning |
| **Mean** | **0.998** | **0.996** | **+0.002** | **0.975** | **0.981** | **-0.006** | (11/15) |

*Δ = Repro - Paper. (Paper values are based on WRN50 backbone results from the original paper)*

## 2. 주요 관찰 사항 (Summary)

- **11차 재현 (2026-05-19):** `grid` I-AUROC 0.998, P-AUROC 0.981 기록. 논문 수치(각각 0.984, 0.983) 대비 I-AUROC에서 +0.014 높은 성능을 보이며 성공적으로 재현됨.
- **10차 재현 (2026-05-19):** `tile` I-AUROC 0.999, P-AUROC 0.961 기록. 논문 수치(각각 0.999, 0.966)와 매우 근접하게 재현됨.
- **9차 재현 (2026-05-18):** `leather` I-AUROC 1.000, P-AUROC 0.992 기록. 논문 수치(각각 1.000, 0.993)와 거의 동일한 수준으로 완벽하게 재현됨.
- **8차 재현 (2026-05-18):** `hazelnut` I-AUROC 0.999, P-AUROC 0.976 기록. I-AUROC는 논문(0.999)과 완벽하게 일치하며, P-AUROC는 소폭 낮음.
- **7차 재현 (2026-05-18):** `cable` I-AUROC 0.999, P-AUROC 0.974 기록. I-AUROC는 논문(0.995)을 상회하였으며, P-AUROC는 소폭 낮음.
- **6차 재현 (2026-05-18):** `transistor` I-AUROC 1.000, P-AUROC 0.969 기록. I-AUROC는 완벽하게 재현되었으며, P-AUROC는 논문(0.977) 대비 소폭 낮음.
- **bottle 재현 업데이트 (2026-05-18):** `batchsize 8`, `resize 329`, `imagesize 288` 설정으로 재실행 결과 I-AUROC 1.000, P-AUROC 0.980 기록. P-AUROC가 이전 대비 소폭 상승(0.978 → 0.980)함.
- **toothbrush 재현 업데이트 (2026-05-18):** `batchsize 8`, `resize 329`, `imagesize 288` 설정으로 재실행 결과 I-AUROC 0.997, P-AUROC 0.984 기록. 논문 수치와 완벽하게 일치하거나 상회함.
- **4차 재현 (2026-05-18):** `wood` I-AUROC 1.000, P-AUROC 0.940 기록. P-AUROC가 논문(0.949) 대비 소폭 낮으나 I-AUROC는 완벽하게 재현됨.
- **3차 재현 (2026-05-18):** `metal_nut` I-AUROC 1.000, P-AUROC 0.986 기록. 논문 설정과 동일하게 `batchsize 8`, `resize 329`, `imagesize 288`로 조정하여 수행.
- **1차 재현 (2026-05-16 ~ 17):** `toothbrush` I-AUROC 1.000, P-AUROC 0.985로 논문 수치(각각 0.991, 0.984)를 상회하거나 동등한 수준 기록.
- **2차 재현 (2026-05-17):** `bottle` I-AUROC 1.000, P-AUROC 0.978로 논문 수치(각각 1.000, 0.982) 대비 P에서 -0.004 격차.
- **시각화 패치:** `main.py` 내의 테스트 로직 버그를 수정하여 히트맵(Segmentation) 이미지가 정상적으로 저장되도록 조치함.
- **향후 계획:** 나머지 6개 카테고리(capsule, carpet, grid, screw, tile, zipper)에 대해 논문 파라미터(batch 8, size 288)를 준수하여 순차적으로 실험을 완료할 예정. 모든 카테고리 재현 완료 후 Method 3 (Reverse Distillation) 프로젝트로 전환하여 `toothbrush` 카테고리부터 baseline 재현을 시도할 계획.
