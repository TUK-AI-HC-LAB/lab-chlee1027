# method1_patchcore — 실행 가이드 및 재현 결과

PatchCore (Roth et al. 2022) baseline을 MVTec AD에서 재현하기 위한 디렉토리입니다.

## 📊 재현 결과 요약 (2026-05-12)

MVTec AD 15개 전 카테고리에 대해 논문 수치와 동등하거나 그 이상의 성능으로 재현을 완료하였습니다.

| Metric | Repro (Mean) | Paper (Mean) | Status |
| :--- | :---: | :---: | :---: |
| **I-AUROC** | **0.992** | 0.991 | ✅ Success |
| **P-AUROC** | **0.982** | 0.981 | ✅ Success |

*상세 수치는 [baseline_full_table.md](../markdown/baseline_full_table.md)에서 확인 가능합니다.*

## 🔍 집중 분석 및 향후 계획

일부 카테고리에서 나타난 미세한 차이를 분석하기 위한 검증 실험이 계획되어 있습니다. 상세 내용은 [repro_failure_analysis.md](../markdown/repro_failure_analysis.md)를 참고하세요.

1. **Pill (I-AUROC Δ -0.011):** Coreset Sampling 비율(10% -> 25%, 100%)에 따른 성능 회복 여부 검증 예정.
2. **Metal_nut (P-AUROC Δ -0.008):** 픽셀 정밀도 향상 실험(해상도 상향 등) 예정.
3. **Screw (I-AUROC Δ +0.018):** 논문 대비 높은 성능의 원인 분석.

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
- `source/run_baseline.sh`: 카테고리별 실험 자동화 쉘 스크립트.
- `source/results/`: 재현 결과 CSV 파일들.
- `markdown/`: 상세 분석 보고서 및 결과 테이블.
- `source/patchcore_colab.ipynb`: 원본 Colab 실험 노트.
