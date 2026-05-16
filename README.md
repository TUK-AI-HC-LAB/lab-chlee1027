## 다루는 method

| # | 폴더 | 논문 | 상태 |
|---|------|------|------|
| 1 | [method1_patchcore](method1_patchcore/source/) | Roth et al., 2022, *Towards Total Recall in Industrial Anomaly Detection* (CVPR 2022, PatchCore) | MVTec AD 15개 전 카테고리 재현 완료 (I-AUROC 0.992) |
| 2 | [method2_simplenet](method2_simplenet/source/) | Liu et al., 2023, *SimpleNet: A Simple Network for Image Anomaly Detection and Localization* (CVPR 2023) | 1차 재현 완료 (toothbrush 단일, I-AUROC 1.000 / P-AUROC 0.983) |

## 진행 상황 요약

- **2026-W18 (4/30 미팅)** — 첫 미팅 참관. 본격 진행은 W19부터.
- **2026-W19 (5/7 미팅)** — PatchCore baseline 재현 (Colab T4). bottle/leather 모두 논문 수치 ±0.005 내 재현. → [meetings/2026-W19_brief.md](meetings/2026-W19_brief.md)
- **2026-W20 (5/14 미팅)** — **PatchCore 전 카테고리(15개) 재현 완료.** 평균 I-AUROC 0.992 기록. `pill`, `metal_nut` 등 미세 하락 항목에 대한 원인 분석 및 검증 실험 보고서 완결. → [meetings/2026-W20_brief.md](meetings/2026-W20_brief.md)
- **2026-W21 (5/21 미팅 예정)** — PatchCore 프로젝트 최종 문서화 및 환경 재현성 확보 계획 검토. → [meetings/2026-W21_brief.md](meetings/2026-W21_brief.md)

## 빠른 링크

- [PatchCore 상세 결과 및 가이드](method1_patchcore/source/README.md)
- [WEEKLY_LOG.md](WEEKLY_LOG.md)
- [meetings/](meetings/)
