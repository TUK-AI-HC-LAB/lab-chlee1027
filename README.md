## 다루는 method

| # | 폴더 | 논문 | 상태 |
|---|------|------|------|
| 1 | [method1_patchcore](method1_patchcore/source/) | Roth et al., 2022, Towards Total Recall in Industrial Anomaly Detection (CVPR 2022, PatchCore) | 재현 완료 (MVTec AD: 15/15 카테고리) |
| 2 | [method2_simplenet](method2_simplenet/source/) | Liu et al., 2023, SimpleNet: A Simple Network for Image Anomaly Detection and Localization (CVPR 2023) | 재현 진행 중 (MVTec AD: 12/15 카테고리) |
| 3 | [method3_RD](method3_RD/source/) | Deng et al., 2022, Anomaly Detection via Reverse Distillation from One-Class Embedding (CVPR 2022, RD) | 분석 및 구조 생성 완료 (실험 예정) |

## 진행 상황 요약

- **2026-W18 (4/30 미팅)** — 첫 미팅 참관. 본격 진행은 W19부터.
- **2026-W19 (5/7 미팅)** — PatchCore baseline 재현 (Colab T4). bottle/leather 모두 논문 수치 ±0.005 내 재현. → [meetings/2026-W19_brief.md](meetings/2026-W19_brief.md)
- **2026-W20 (5/14 미팅)** — **PatchCore 전 카테고리(15개) 재현 완료.** 평균 I-AUROC 0.992 기록. `pill`, `metal_nut` 등 미세 하락 항목에 대한 원인 분석 및 검증 실험 보고서 완결. → [meetings/2026-W20_brief.md](meetings/2026-W20_brief.md)
- **2026-W21 (5/21 미팅 예정)** — PatchCore 프로젝트 최종 문서화 및 환경 재현성 확보 계획 검토. **SimpleNet 1~12차 재현 (12/15) 완료. 논문 동일 환경 설정 반영.** method3 Reverse Distillation 착수. → [meetings/2026-W21_brief.md](meetings/2026-W21_brief.md)

## 빠른 링크

- [PatchCore 상세 결과 및 가이드](method1_patchcore/source/README.md)
- [SimpleNet 통합 결과 테이블](method2_simplenet/markdown/baseline_full_table.md)
- [WEEKLY_LOG.md](WEEKLY_LOG.md)
- [meetings/](meetings/)
