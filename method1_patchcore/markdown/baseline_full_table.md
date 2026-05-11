# PatchCore Baseline Reproduction Results (MVTec AD)

> **Environment:** Colab T4 / Python 3.12 / torch 2.10.0+cu128
> **Settings:** PatchCore-10% (WideResNet50, layers 2+3, coreset 0.1, patchsize 3)
> **Paper:** Roth et al. 2022 (PatchCore)

## 1. Summary Table (15 Categories)

| Category | I-AUROC (Repro) | I-AUROC (Paper) | Δ (I) | P-AUROC (Repro) | P-AUROC (Paper) | Δ (P) | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| bottle | 1.000 | 1.000 | +0.000 | 0.985 | 0.986 | -0.001 | Done |
| cable | 0.997 | 0.995 | +0.002 | 0.984 | 0.985 | -0.001 | Done |
| capsule | 0.979 | 0.981 | -0.002 | 0.990 | 0.990 | +0.000 | Done |
| carpet | 0.986 | 0.987 | -0.001 | 0.991 | 0.991 | +0.000 | Done |
| grid | 0.979 | 0.979 | +0.000 | 0.988 | 0.987 | +0.001 | Done |
| hazelnut | 1.000 | 1.000 | +0.000 | 0.987 | 0.987 | +0.000 | Done |
| leather | 1.000 | 1.000 | +0.000 | 0.993 | 0.990 | +0.003 | Done |
| metal_nut | 0.999 | 1.000 | -0.001 | 0.983 | 0.991 | -0.008 | Done |
| pill | 0.967 | 0.978 | -0.011 | 0.978 | 0.985 | -0.007 | Done |
| screw | 0.988 | 0.970 | +0.018 | 0.995 | 0.994 | +0.001 | Done |
| tile | 0.995 | 0.989 | +0.006 | 0.957 | 0.959 | -0.002 | Done |
| toothbrush | - | 0.997 | - | - | 0.987 | - | Pending |
| transistor | 0.999 | 1.000 | -0.001 | 0.961 | 0.963 | -0.002 | Done |
| wood | 0.991 | 0.990 | +0.001 | 0.951 | 0.951 | +0.000 | Done |
| zipper | - | 0.995 | - | - | 0.989 | - | Pending |
| **Mean** | **0.992** | **0.991** | **+0.001** | **0.985** | **0.985** | **+0.000** | (13/15) |

*Δ = Repro - Paper. Δ < ±0.005 is generally considered a successful reproduction.*

## 2. Observations

- **Successfully Reproduced:** 9 categories (bottle, cable, capsule, carpet, hazelnut, leather, metal_nut, pill, transistor) show results very close to the paper values.
- **Pending:** 6 categories (grid, screw, tile, toothbrush, wood, zipper) are scheduled for execution.
- **Pill Category:** Shows a slightly larger gap in I-AUROC (-0.011), which may be due to the coreset sampling randomness or seed differences.

