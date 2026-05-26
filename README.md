## 다루는 method

| # | 폴더 | 논문 | 상태 |
|---|------|------|------|
| 1 | [method1_patchcore](method1_patchcore/source/) | Roth et al., 2022, Towards Total Recall in Industrial Anomaly Detection (CVPR 2022, PatchCore) | 재현 완료 (MVTec AD: 15/15 카테고리) |
| 2 | [method2_simplenet](method2_simplenet/source/) | Liu et al., 2023, SimpleNet: A Simple Network for Image Anomaly Detection and Localization (CVPR 2023) | 재현 완료 (MVTec AD: 15/15 카테고리) |
| 3 | [method3_RD](method3_RD/source/) | Deng et al., 2022, Anomaly Detection via Reverse Distillation from One-Class Embedding (CVPR 2022, RD) | 재현 완료 (MVTec AD: 15/15 카테고리) |
| 4 | [method4_Dinomaly](method4_Dinomaly/source/) | Guo et al., 2025, Dinomaly: The Less Is More Philosophy in Multi-Class Unsupervised Anomaly Detection (CVPR 2025) | 재현 완료 (MVTec AD: 15/15 카테고리) |

## 진행 상황 요약

- **2026-W18 (4/30 미팅)** — 첫 미팅 참관. 본격 진행은 W19부터.
- **2026-W19 (5/7 미팅)** — PatchCore baseline 재현 (Colab T4). bottle/leather 모두 논문 수치 ±0.005 내 재현. → [meetings/2026-W19_brief.md](meetings/2026-W19_brief.md)
- **2026-W20 (5/14 미팅)** — **PatchCore 전 카테고리(15개) 재현 완료.** 평균 I-AUROC 0.992 기록. `pill`, `metal_nut` 등 미세 하락 항목에 대한 원인 분석 및 검증 실험 보고서 완결. → [meetings/2026-W20_brief.md](meetings/2026-W20_brief.md)
- **2026-W21 (5/21 미팅)** — **SimpleNet 전 카테고리(15/15) 재현 완료** + PatchCore 최종 문서화. **method3 Reverse Distillation 착수 14/15 재현 진행 중**, 3-way 비교 문서 작성. → [meetings/2026-W21_brief.md](meetings/2026-W21_brief.md)
- **2026-W22 (5/28 미팅 예정)** — **Reverse Distillation 전 카테고리(15/15) 완결 및 분석 보고.** (5/22 완료) **method4 Dinomaly 전 카테고리(15/15) 재현 완료 및 수치 검증(Mean I-AUROC 0.9962).** SimpleNet 구조적 약점 분석(screw/capsule) 및 4-way 비교 프레임워크 설계 완료. → [meetings/2026-W22_brief.md](meetings/2026-W22_brief.md)

## 빠른 링크

- [method1 PatchCore — 가이드·결과](method1_patchcore/source/README.md)
- [method2 SimpleNet — 가이드·결과](method2_simplenet/source/README.md)
- [method3 RD — 가이드·결과](method3_RD/source/README.md)
- [method4 Dinomaly — 가이드·결과](method4_Dinomaly/source/README.md)
- [3-way 비교 (PatchCore·SimpleNet·RD)](method3_RD/markdown/rd_vs_patchcore_simplenet.md)
- [4-way 비교 (추후 작성 예정)]
- [WEEKLY_LOG.md](WEEKLY_LOG.md)
- [meetings/](meetings/)
