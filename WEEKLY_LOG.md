# Weekly Log

## 2026-W21 (5/15 ~ 5/21, 5/21 미팅)
- 미팅 자료: [meetings/2026-W21_brief.md](meetings/2026-W21_brief.md)

### 전주 계획 달성도
- [x] **PatchCore 프로젝트 최종 문서화 및 환경 재현성 검토 완결 (2026-05-16)**
- [x] **코랩 T4 환경 스냅샷(requirements.txt) 및 결과 시각화 반영 완료**
- [x] **method2_simplenet 폴더 구조 생성 + 논문 요약 작성** → [`method2_simplenet/markdown/simplenet_summary.md`](method2_simplenet/markdown/simplenet_summary.md)
- [x] **SimpleNet 1·2차 재현 + 시각화 버그 수정 완료 (2026-05-16 ~ 17)**
  - 5/16 toothbrush 1차: I-AUROC 1.000 / P-AUROC 0.983 / Anomaly P 0.904 (시각화 미생성 이슈 발견)
  - 5/17 시각화 패치 후 재실행:
    - toothbrush: I-AUROC 1.000 / P-AUROC **0.985** / Anomaly P **0.915** (패치 후 P 두 지표 모두 소폭 상승)
    - bottle (신규): I-AUROC 1.000 / P-AUROC 0.978 / Anomaly P 0.915
  - 시각화: `main.py` 버그 패치 후 히트맵 생성 성공 (노트북 내 출력 확인)
  - 노트북: `method2_simplenet/source/simplenet_colab.ipynb` (실행 결과 포함 업데이트)
  - 결과 csv: `method2_simplenet/source/results/baseline_toothbrush.csv` (5/16, 5/17 통합), `baseline_bottle.csv`
  - 통합 테이블: [`method2_simplenet/markdown/baseline_full_table.md`](method2_simplenet/markdown/baseline_full_table.md) (이 시점 2/15 → 이후 15/15 완결)
  - 수정 사항 3건: `metrics.py` (pandas 호환), `main.py` (시각화 활성화), `simplenet_colab.ipynb` (자동 실행 셀 + 결과 수직 나열)
- [x] **SimpleNet 3~11차 확장 재현 수행 (2026-05-18 ~ 19)**
  - 5/18 (3~9차): `metal_nut`, `wood`, `transistor`, `cable`, `hazelnut`, `leather` 등 7개 카테고리 추가 완료
  - 5/19 (10~15차): `tile`, `grid`, `capsule`, `screw`, `zipper`, `carpet` 카테고리 추가 완료 (15/15 완결)
  - 모든 실험은 논문 동일 설정(`batchsize 8`, `resize 329`, `imagesize 288`) 적용
  - 통합 테이블 및 개별 CSV 실시간 업데이트 및 푸시 완료
- [x] **method3_RD 프로젝트 착수 (2026-05-18)**
  - 논문 분석 및 요약 완료: [`method3_RD/markdown/rd_summary.md`](method3_RD/markdown/rd_summary.md)
  - 폴더 구조 및 기본 README 생성 완료
  - 바탕 화면의 논문 PDF를 `method3_RD/paper/`로 이동 정비

### 이전 미팅 결정 사항 (5/14)
- README 및 문서의 '계획 중' 상태를 '완료'로 최신화
- PyTorch/CUDA 버전 차이에 따른 재현성 확보를 위한 기술적 계획 수립 (requirements 스냅샷 등)
- `pill`, `metal_nut` 분석 보고서 최종 완결

### 다음 미팅까지의 계획 (측정 가능한 단위로)
- **SimpleNet ↔ PatchCore 비교 분석** — 15개 카테고리 결과를 나란히 둔 비교표 + 분석 노트 `method2_simplenet/markdown/simplenet_vs_patchcore.md` (특히 pill·metal_nut에서 SimpleNet 우위 분석)
- **SimpleNet 노트북 → 셸 스크립트화** — `method2_simplenet/source/run_baseline.sh` (CATEGORY 환경변수), 재현 출처 commit/sh/csv 3줄 완성
- **method3_RD 실험 착수** — upstream(`hqucl/Reverse-Distillation`) 코드 분석 + bottle·toothbrush 우선 baseline 실행

---

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

### 이전 미팅 결정 사항 (5/14)
- README 및 문서의 '계획 중' 상태를 '완료'로 최신화
- PyTorch/CUDA 버전 차이에 따른 재현성 확보를 위한 기술적 계획 수립 (requirements 스냅샷 등)
- `pill`, `metal_nut` 분석 보고서 최종 완결

### 다음 미팅까지의 계획 (측정 가능한 단위로)
- **PatchCore 프로젝트 최종 문서화 점검** — 신규 수립된 [환경 재현성 계획](method1_patchcore/markdown/environment_reproducibility_plan.md) 검토 및 보완
- **SimpleNet 확장 준비** — `method2_simplenet/` 폴더 생성 + 논문 PDF·요약 작성 (완료, [method2_simplenet/markdown/simplenet_summary.md](method2_simplenet/markdown/simplenet_summary.md))

---

## 2026-W19 (5/1 ~ 5/7, 5/7 미팅)
- 미팅 자료: [meetings/2026-W19_brief.md](meetings/2026-W19_brief.md)

### 전주 계획 달성도
- [x] PatchCore (Roth et al. 2022) baseline 재현 — bottle/leather 4개 지표 전부 논문 수치 ±0.005 이내 재현 성공
  - 결과: `method1_patchcore/source/results/baseline_bottle_20260506.csv`, `method1_patchcore/source/results/baseline_leather_20260506.csv`
  - 분석: `method1_patchcore/markdown/baseline_analysis.md`
  - 실행: `method1_patchcore/source/run_baseline.sh` (CATEGORY=bottle/leather)

### 이전 미팅 결정 사항 (5/7)
- 정식 첫 미팅 — bottle/leather 재현 보고. 미팅 직후 지도교수 피드백 수신
- 다음 주 우선순위: PatchCore MVTec AD 전 카테고리(15개) 확장 재현
- 개선 필요: 점진 push 습관 정착 (W19 commit이 5/6 하루에 몰린 점)
- (상세는 W20 brief에 반영)

### 다음 미팅까지의 계획 (측정 가능한 단위로)
- 상세는 [meetings/2026-W20_brief.md](meetings/2026-W20_brief.md) 참고

---

## 2026-W18 (4/23 ~ 4/30, 4/30 미팅)
- 미팅 자료: 없음 (참관 미팅)

### 이전 미팅 결정 사항 (4/30)
- 시작 method는 PatchCore (Roth et al. 2022) baseline 재현으로 결정 — `method1_patchcore/`


