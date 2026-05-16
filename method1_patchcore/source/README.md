# method1_patchcore — 실행 가이드 및 재현 결과

PatchCore (Roth et al. 2022) baseline을 MVTec AD에서 재현하기 위한 디렉토리입니다.

## 📊 재현 결과 요약 (2026-05-12)

MVTec AD 15개 전 카테고리에 대해 논문 수치와 동등하거나 그 이상의 성능으로 재현을 완료하였습니다.

| Metric | Repro (Mean) | Paper (Mean) | Status |
| :--- | :---: | :---: | :---: |
| **I-AUROC** | **0.992** | 0.991 | ✅ Success |
| **P-AUROC** | **0.982** | 0.981 | ✅ Success |

*상세 수치는 [baseline_full_table.md](../markdown/baseline_full_table.md)에서 확인 가능합니다.*

## 🔍 집중 분석 및 결과 보고

일부 카테고리에서 나타난 미세한 차이를 분석하기 위한 검증 실험과 원인 규명을 완료하였습니다. 상세 내용은 다음 문서들을 참고하세요.

1. **[repro_failure_analysis.md](../markdown/repro_failure_analysis.md):** `pill`, `metal_nut` 하락 원인 분석 및 검증 결과 보고서 (완결)
2. **[environment_reproducibility_plan.md](../markdown/environment_reproducibility_plan.md):** PyTorch/CUDA 환경 차이에 따른 재현성 확보를 위한 기술적 대응 계획 (신규)

---

## 💻 환경 및 실행 가이드

### 환경 (Colab T4 기준)
- Python 3.12, CUDA 12.x
- PyTorch 2.10.0+cu128 (Colab 기본)
- faiss-cpu 1.13.2
- `requirements.txt` 참고. Colab 환경에선 `faiss-cpu`만 추가 설치하면 됩니다.

### 데이터 준비
MVTec AD 데이터셋을 다음 구조로 배치하세요.
```
<MVTEC_DIR>/
├── bottle/
│   ├── train/good/...
│   └── test/{good,broken_large,...}/...
└── ...
```
- **Colab:** Google Drive 마운트 후 경로 지정.
- **로컬:** `MVTEC_DIR` 환경변수 또는 인자로 경로 지정.

### 실행 방법
```bash
# 특정 카테고리 실행 (예: bottle)
CATEGORY=bottle MVTEC_DIR=/path/to/mvtec bash run_baseline.sh
```
**스크립트 동작 과정:**
1. upstream [amazon-science/patchcore-inspection](https://github.com/amazon-science/patchcore-inspection)을 clone.
2. 본 repo의 `source/run_patchcore.py`를 upstream의 `bin/run_patchcore.py`에 덮어쓰기하여 수정사항 적용.
3. 표준 PatchCore-10% 설정(WRN-50, layer2+3, coreset 10%, NN=1, patchsize=3)으로 실행.

## 🛠 수정 내역 (upstream 대비)

`run_patchcore.py`의 시각화 함수(`image_transform`)에서 데이터셋 속성 접근 오류를 해결하기 위해 ImageNet 표준 정규화 값을 직접 명시하도록 수정되었습니다. 이 변경은 메트릭(AUROC) 계산에는 영향을 주지 않습니다.

**원본 (Upstream)**:
```python
def image_transform(image):
    in_std = np.array(
        dataloaders["testing"].dataset.transform_std
    ).reshape(-1, 1, 1)
    in_mean = np.array(
        dataloaders["testing"].dataset.transform_mean
    ).reshape(-1, 1, 1)
    image = dataloaders["testing"].dataset.transform_img(image)
    return np.clip(
        (image.numpy() * in_std + in_mean) * 255, 0, 255
    ).astype(np.uint8)
```

**수정 후 (Actual implementation)**:
```python
def image_transform(image):
    in_std = np.array([0.229, 0.224, 0.225]).reshape(-1, 1, 1)
    in_mean = np.array([0.485, 0.456, 0.406]).reshape(-1, 1, 1)

    image = dataloaders["testing"].dataset.transform_img(image)

    return np.clip((image.numpy() * in_std + in_mean) * 255, 0, 255).astype(np.uint8)
```

## 📂 파일 구조
- `source/run_patchcore.py`: 수정된 메인 실행 스크립트.
- `source/run_baseline.sh`: 카테고리별 baseline 자동화 쉘 스크립트.
- `source/run_validation.sh`: pill·metal_nut 검증 실험(샘플링/해상도/레이어 스윕) 자동화 쉘 스크립트.
- `source/apply_modifications.py`: upstream `bin/run_patchcore.py`에 수정사항을 idempotent하게 적용하는 fallback 패치.
- `source/results/`: 재현 결과 CSV (baseline 15개 + 검증 실험 2개).
- `markdown/`: 상세 분석 보고서 및 결과 테이블.
- `source/patchcore_colab.ipynb`: 원본 Colab 실험 노트.

## 📌 재현 출처 (가이드 형식 — commit/sh/csv 3줄)

### Baseline 15개 카테고리

- bottle / leather (5/6 실행)
  - commit: `553b14f`
  - sh: `method1_patchcore/source/run_baseline.sh` (CATEGORY=bottle / leather)
  - csv: `method1_patchcore/source/results/baseline_bottle_20260506.csv`, `baseline_leather_20260506.csv`
- 그 외 13개 카테고리 (5/10~5/11 실행)
  - commit: `8bf1630`
  - sh: `method1_patchcore/source/run_baseline.sh` (CATEGORY=cable, capsule, carpet, grid, hazelnut, metal_nut, pill, screw, tile, toothbrush, transistor, wood, zipper)
  - csv: `method1_patchcore/source/results/baseline_<category>_<date>.csv` (13개)
- 집계표: [`method1_patchcore/markdown/baseline_full_table.md`](../markdown/baseline_full_table.md)

### Validation 실험 (pill 샘플링 역설, metal_nut 해상도/레이어 영향)

- pill 종합 스윕
  - commit: `57e9a11`
  - sh: `method1_patchcore/source/run_validation.sh`
  - csv: `method1_patchcore/source/results/val_pill_total_study.csv`
- metal_nut 종합 스윕
  - commit: `7c9a723`
  - sh: `method1_patchcore/source/run_validation.sh`
  - csv: `method1_patchcore/source/results/val_metal_nut_total_study.csv`
- 분석 보고서: [`method1_patchcore/markdown/repro_failure_analysis.md`](../markdown/repro_failure_analysis.md)
