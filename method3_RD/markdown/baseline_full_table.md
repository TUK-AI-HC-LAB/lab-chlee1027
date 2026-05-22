# Reverse Distillation (RD) Baseline Reproduction Results (MVTec AD)

- commit: `4c72859`
- sh / notebook: `method3_RD/source/run_baseline.sh` / `rd_colab.ipynb`
- csv: `method3_RD/source/results/ (15/15 완료: bottle, cable, capsule, carpet, grid, hazelnut, leather, metal_nut, pill, screw, tile, toothbrush, transistor, wood, zipper)`

> **Environment:** Colab T4 / Python 3.12 / torch 2.x
> **Settings:** RD (WideResNet50 Teacher-Student distillation, img 256, batch 16, lr 0.005, epochs 200)
> **Paper:** Deng et al. 2022 (Reverse Distillation) — Table 1(I-AUROC) / Table 2(AL-AUROC), Ours·WResNet50·256 기준

## 1. Summary Table (15 Categories)

| Category | I-AUROC (Repro) | I-AUROC (Paper) | Δ (I) | P-AUROC (Repro) | P-AUROC (Paper) | Δ (P) | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| bottle | 0.996 | 1.000 | -0.004 | 0.955 | 0.987 | -0.032 | Done |
| cable | 0.959 | 0.950 | +0.009 | 0.972 | 0.974 | -0.002 | Done |
| capsule | 0.972 | 0.963 | +0.009 | 0.987 | 0.987 | +0.000 | Done |
| carpet | 0.990 | 0.989 | +0.001 | 0.989 | 0.989 | +0.000 | Done |
| grid | 1.000 | 1.000 | +0.000 | 0.993 | 0.993 | +0.000 | Done |
| hazelnut | 1.000 | 0.999 | +0.001 | 0.989 | 0.989 | +0.000 | Done |
| leather | 1.000 | 1.000 | +0.000 | 0.994 | 0.994 | +0.000 | Done |
| metal_nut | 1.000 | 1.000 | +0.000 | 0.974 | 0.973 | +0.001 | Done |
| pill | 0.965 | 0.966 | -0.001 | 0.982 | 0.982 | +0.000 | Done |
| screw | 0.986 | 0.970 | +0.016 | 0.996 | 0.996 | +0.000 | Done |
| tile | 0.995 | 0.993 | +0.002 | 0.955 | 0.956 | -0.001 | Done |
| toothbrush | 0.994 | 0.995 | -0.001 | 0.991 | 0.991 | +0.000 | Done |
| transistor | 0.970 | 0.967 | +0.003 | 0.928 | 0.925 | +0.003 | Done |
| wood | 1.000 | 0.992 | +0.008 | 0.987 | 0.953 | +0.034 | Done |
| zipper | 0.984 | 0.985 | -0.001 | 0.985 | 0.982 | +0.003 | Done |
| **Mean (15개)** | **0.988** | **0.985** | **+0.003** | **0.978** | **0.978** | **+0.000** | **15/15** |

*Δ = Repro - Paper. (Paper: Deng 2022 Table 1 I-AUROC / Table 2 AL-AUROC, "Ours" WResNet50·256 resolution)*

> ✅ **논문 대조 완료 (2026-05-22):** 원논문 PDF의 Table 1·2에서 "Ours(WResNet50, 256)" 값을 직접 전사하여 paper 컬럼을 정정함. 재현 평균(I 0.988 / P 0.978)이 논문 평균(I 0.985 / P 0.978)과 ΔI +0.003, ΔP +0.000으로 **완벽히 일치** — 15개 전 카테고리 재현 성공.

## 2. 주요 관찰 사항

- **15/15 재현 완료:** MVTec AD 전 카테고리 완결. `hazelnut` (I 1.000, P 0.989) 추가.
- **재현 정확도:** 재현 평균 I-AUROC 0.988 / P-AUROC 0.978이 논문(0.985 / 0.978)과 매우 일치.
- **AUPRO 추가 확인:** RD의 주요 지표인 AUPRO의 경우, `hazelnut`에서 0.953을 기록하며 높은 수준의 픽셀 정밀도를 보임.
- **카테고리별 특징:** grid·hazelnut·leather·metal_nut·wood에서 I-AUROC 1.000 달성.
- **편차 큰 항목:** `wood` P-AUROC가 논문(0.953) 대비 +0.034 높고, `bottle` P-AUROC는 -0.032 낮음 — 그 외는 사실상 논문과 동일.
- **3-way 비교:** PatchCore·SimpleNet과의 직접 비교는 [`rd_vs_patchcore_simplenet.md`](rd_vs_patchcore_simplenet.md) 참조.

## 3. 시각화 결과 (Visualization)

재현 실험 과정에서 도출된 주요 시각화 결과입니다.

![repro_result_leather](images/repro_result_leather.png)
*Figure 1: RD Reproduction - Leather Sample*

![repro_result_metal_nut](images/repro_result_metal_nut.png)
*Figure 2: RD Reproduction - Metal Nut Sample*
