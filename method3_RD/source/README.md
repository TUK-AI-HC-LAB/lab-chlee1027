# method3_RD — 실행 가이드 및 재현 결과

Reverse Distillation (Deng et al. 2022, *Anomaly Detection via Reverse Distillation from One-Class Embedding*, CVPR 2022) baseline을 MVTec AD에서 재현하기 위한 디렉토리입니다.

## 📊 재현 결과 요약 (2026-05-21)

MVTec AD **13/15 카테고리** 재현 완료 (hazelnut·pill 진행 중).

| Metric | Repro (Mean, 13개) | Status |
| :--- | :---: | :---: |
| **I-AUROC** | **0.988** | 🔄 13/15 |
| **Full P-AUROC** | **0.977** | 🔄 13/15 |

*RD의 3번째 픽셀 지표는 AUPRO(Per-Region Overlap)이며, 카테고리별 상세는 [baseline_full_table.md](../markdown/baseline_full_table.md) 참조.*

## 🔍 집중 분석 및 결과 보고

1. **[baseline_analysis.md](../markdown/baseline_analysis.md):** 12/15 카테고리 재현 분석 (개요/환경/종합 결과/관찰/결론)
2. **[baseline_full_table.md](../markdown/baseline_full_table.md):** 카테고리별 재현 결과표 + 시각화
3. **[rd_summary.md](../markdown/rd_summary.md):** 논문 요약 + 핵심 구조(Teacher-Student / OCBE / 복원 오차) + PatchCore·SimpleNet과의 차별점
4. **[rd_vs_patchcore_simplenet.md](../markdown/rd_vs_patchcore_simplenet.md):** PatchCore·SimpleNet·RD 3-way 비교 분석

---

## 💻 환경 및 실행 가이드

### 환경 (Colab T4 기준)
- Python 3.12, CUDA 12.x
- PyTorch 2.x (Colab 기본)
- scipy, scikit-learn, scikit-image, matplotlib
- upstream: [hq-deng/RD4AD](https://github.com/hq-deng/RD4AD) (공식 구현체)

### 데이터 준비
method1·2와 동일한 MVTec AD 구조. RD4AD는 코드 루트의 `mvtec/` 폴더를 참조하므로 심볼릭 링크로 대응.
```
RD4AD/mvtec/
├── bottle/
├── toothbrush/
└── ...
```
- **Colab:** Google Drive 마운트 후 `/content/drive/MyDrive/anormaly_detection/mvtec`를 `RD4AD/mvtec`로 symlink.
- **로컬:** lab repo 루트의 `mvtec_anomaly_detection/` 활용.

### 실행 방법
```bash
# 특정 카테고리 실행 (예: leather)
CATEGORY=leather MVTEC_DIR=/path/to/mvtec bash run_baseline.sh
```
**스크립트/노트북 동작 과정:**
1. upstream [hq-deng/RD4AD](https://github.com/hq-deng/RD4AD)을 clone.
2. `test.py`(pandas 호환) 수정사항 적용.
3. `main_single.py`로 단일 카테고리 학습+평가 (RD4AD `main.py`는 전 카테고리 순회형이라 단일 실행용 래퍼 사용).

> 1차 탐색은 노트북(`rd_colab.ipynb`)으로 진행. 학습 설정: img 256, batch 16, lr 0.005, epochs 200.

## 🛠 수정 내역 (upstream 대비)

총 2건. 메트릭 계산 경로엔 영향 없음.

1. **`test.py`**: pandas 2.0+ 호환. `df.append()`를 `pd.concat()`으로 교체.
   ```python
   # 원본
   df = df.append({"pro": mean(pros), "fpr": fpr, "threshold": th}, ignore_index=True)
   # 수정 후
   df = pd.concat([df, pd.DataFrame([{"pro": mean(pros), "fpr": fpr, "threshold": th}])], ignore_index=True)
   ```
2. **`main_single.py` (신규 래퍼)**: RD4AD `main.py`가 전 카테고리를 순회하므로, `train(<category>)`만 호출하는 단일 카테고리 실행 래퍼를 생성해 카테고리별로 실행.

## 📂 폴더 구조 및 파일 가이드
- `source/run_baseline.sh`: 카테고리별 실험 자동화 쉘 스크립트 (upstream clone + 패치 + 단일 카테고리 실행).
- `source/rd_colab.ipynb`: 실험 및 시각화 검증용 Colab 노트.
- `source/requirements.txt`: Colab T4 환경 패키지 스냅샷.
- `source/results/`: 재현 결과 CSV (현재 13개 카테고리).
- `markdown/`: 논문 요약, 재현 분석, 결과 테이블, 3-way 비교, 시각화.

## 📌 재현 출처 (가이드 형식 — commit/sh/csv 3줄)

### MVTec AD 13/15 카테고리 (진행 중)

- commit: `8286d39`
- sh / 노트북: `method3_RD/source/run_baseline.sh` (CATEGORY 환경변수) / `rd_colab.ipynb`
- csv: `method3_RD/source/results/baseline_<category>_0521.csv` (13개)
- 집계표: [`method3_RD/markdown/baseline_full_table.md`](../markdown/baseline_full_table.md)
