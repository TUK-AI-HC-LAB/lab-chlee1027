# Weekly Log

## 2026-W20 (5/8 ~ 5/14, 5/14 미팅)
- 미팅 자료: [meetings/2026-W20_brief.md](meetings/2026-W20_brief.md)

### 전주 계획 달성도
- [x] W19 피드백 반영 완료
- [x] method1: PatchCore MVTec AD 전 카테고리(15개) 재현 (15/15 완료)
- [x] 성능 하락 원인 분석 및 검증 실험 수행
  - [x] Pill: 샘플링 비율/시드/레이어 실험 완료 (`method1_patchcore/source/results/val_pill_total_study.csv`)
  - [x] Metal_nut: 해상도/레이어 실험 완료 (`method1_patchcore/source/results/val_metal_nut_total_study.csv`)
  - [x] 검증 자동화 스크립트 작성 (`method1_patchcore/source/run_validation.sh`)
- [x] 차기 주차 미팅 자료 준비 (`meetings/2026-W21_brief.md`)

### 이전 미팅 결정 사항 (5/7)
- Pill/Metal_nut 하락 원인 규명 집중

### 다음 미팅까지의 계획 (측정 가능한 단위로)
- **PatchCore 재현 프로젝트 마무리 및 보고**
  - 실험 데이터 최종 검토 및 `repro_failure_analysis.md` 완결
- **신규 Method 조사**
  - PatchCore 이후 다룰 차세대 이상탐지 알고리즘(예: EfficientAD 또는 FastFlow) 후보 2종 선정 및 초안 작성

---

## 2026-W19 (5/1 ~ 5/7, 5/7 미팅)
- 미팅 자료: [meetings/2026-W19_brief.md](meetings/2026-W19_brief.md)

### 전주 계획 달성도
- [o] PatchCore (Roth et al. 2022) baseline 재현 — bottle/leather 4개 지표 전부 논문 수치 ±0.005 이내 재현 성공
  - 결과: `method1_patchcore/source/results/baseline_bottle_20260506.csv`, `method1_patchcore/source/results/baseline_leather_20260506.csv`
  - 분석: `method1_patchcore/markdown/baseline_analysis.md`
  - 실행: `method1_patchcore/source/run_baseline.sh` (CATEGORY=bottle/leather)

### 이전 미팅 결정 사항 (4/30)
- 시작 method는 PatchCore (Roth et al. 2022) baseline 재현으로 결정 — `method1_patchcore/`

---

## 2026-W18 (4/23 ~ 4/30, 4/30 미팅)
- 미팅 자료: 없음 (참관 미팅)


