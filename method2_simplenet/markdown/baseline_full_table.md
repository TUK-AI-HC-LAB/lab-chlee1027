# SimpleNet Baseline Reproduction Results (MVTec AD)

- commit: `486146d`
- sh / notebook: `method2_simplenet/source/simplenet_colab.ipynb`
- csv: `method2_simplenet/source/results/baseline_toothbrush.csv` (15 categories planned)

> **Environment:** Colab T4 / Python 3.12 / torch 2.10.0+cu128
> **Settings:** SimpleNet (WideResNet50, layers 2+3, patchsize 3, meta_epochs 40, gan_epochs 4)
> **Parameters:** batchsize 8, resize 329, imagesize 288 (Paper matching)
> **Paper:** Liu et al. 2023 (SimpleNet)

## 1. Summary Table (15 Categories)

| Category | I-AUROC (Repro) | I-AUROC (Paper) | Δ (I) | P-AUROC (Repro) | P-AUROC (Paper) | Δ (P) | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| bottle | 1.000 | 1.000 | +0.000 | 0.980 | 0.982 | -0.002 | Done |
| cable | - | 0.995 | - | - | 0.985 | - | Planning |
| capsule | - | 0.985 | - | - | 0.990 | - | Planning |
| carpet | - | 0.992 | - | - | 0.990 | - | Planning |
| grid | - | 0.984 | - | - | 0.983 | - | Planning |
| hazelnut | - | 0.999 | - | - | 0.988 | - | Planning |
| leather | - | 1.000 | - | - | 0.993 | - | Planning |
| metal_nut | 1.000 | 1.000 | +0.000 | 0.986 | 0.981 | +0.005 | Done |
| pill | 0.986 | 0.987 | -0.001 | 0.984 | 0.975 | +0.009 | Done |
| screw | - | 0.992 | - | - | 0.996 | - | Planning |
| tile | - | 0.999 | - | - | 0.966 | - | Planning |
| toothbrush | 0.997 | 0.991 | +0.006 | 0.984 | 0.984 | +0.000 | Done |
| transistor | - | 1.000 | - | - | 0.977 | - | Planning |
| wood | 1.000 | 0.992 | +0.008 | 0.940 | 0.949 | -0.009 | Done |
| zipper | - | 0.998 | - | - | 0.991 | - | Planning |
| **Mean** | **0.997** | **0.996** | **+0.001** | **0.975** | **0.981** | **-0.006** | (5/15) |

*Δ = Repro - Paper. (Paper values are based on WRN50 backbone results from the original paper)*

## 2. 주요 관찰 사항 (Summary)

- **bottle 재현 업데이트 (2026-05-18):** `batchsize 8`, `resize 329`, `imagesize 288` 설정으로 재실행 결과 I-AUROC 1.000, P-AUROC 0.980 기록. P-AUROC가 이전 대비 소폭 상승(0.978 → 0.980)함.
- **5차 재현 (2026-05-18):** `pill` I-AUROC 0.986, P-AUROC 0.984 기록. 논문 수치(각각 0.987, 0.975)와 매우 근접하게 재현됨.
- **toothbrush 재현 업데이트 (2026-05-18):** `batchsize 8`, `resize 329`, `imagesize 288` 설정으로 재실행 결과 I-AUROC 0.997, P-AUROC 0.984 기록. 논문 수치와 완벽하게 일치하거나 상회함.
- **4차 재현 (2026-05-18):** `wood` I-AUROC 1.000, P-AUROC 0.940 기록. P-AUROC가 논문(0.949) 대비 소폭 낮으나 I-AUROC는 완벽하게 재현됨.
- **3차 재현 (2026-05-18):** `metal_nut` I-AUROC 1.000, P-AUROC 0.986 기록. 논문 설정과 동일하게 `batchsize 8`, `resize 329`, `imagesize 288`로 조정하여 수행.
- **1차 재현 (2026-05-16 ~ 17):** `toothbrush` I-AUROC 1.000, P-AUROC 0.985로 논문 수치(각각 0.991, 0.984)를 상회하거나 동등한 수준 기록.
- **2차 재현 (2026-05-17):** `bottle` I-AUROC 1.000, P-AUROC 0.978로 논문 수치(각각 1.000, 0.982) 대비 P에서 -0.004 격차.
- **시각화 패치:** `main.py` 내의 테스트 로직 버그를 수정하여 히트맵(Segmentation) 이미지가 정상적으로 저장되도록 조치함.
- **향후 계획:** 나머지 13개 카테고리에 대해 순차적으로 실험을 진행하여 PatchCore와의 성능 격차를 분석할 예정.
