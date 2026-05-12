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

대부분의 카테고리가 성공적으로 재현되었으나, 일부 카테고리에서 나타난 미세한 차이를 분석하기 위한 추가 실험이 계획되어 있습니다.

1. **Pill (I-AUROC Δ -0.011):** Coreset Sampling 비율(10% -> 25%, 100%)에 따른 성능 회복 여부 검증 예정.
2. **Metal_nut (P-AUROC Δ -0.008):** 금속 반사광 및 나사산 구조에 따른 픽셀 정밀도 향상 실험(해상도 상향 등) 예정.
3. **Screw (I-AUROC Δ +0.018):** 논문 대비 높은 성능의 원인 분석.

상세 분석 내용은 [repro_failure_analysis.md](../markdown/repro_failure_analysis.md)를 참고하세요.

## 환경 (Colab T4 기준)

- Python 3.12, CUDA 12.x
- PyTorch 2.10.0+cu128
- faiss-cpu 1.13.2

## 실행 방법

```bash
# 특정 카테고리 실행 (예: bottle)
CATEGORY=bottle MVTEC_DIR=/path/to/mvtec bash run_baseline.sh
```

- **표준 설정:** WideResNet50, layers 2+3, coreset 10%, NN=1, patchsize=3, resize 256/center 224, seed 0.
- **수정 사항:** 시각화(`image_transform`) 시 발생하는 데이터셋 속성 접근 오류를 해결하기 위해 ImageNet 표준 정규화 값을 직접 명시하도록 수정되었습니다. (메트릭 계산에는 영향 없음)

## 파일 구조

- `source/run_patchcore.py`: 수정된 메인 실행 스크립트.
- `source/run_baseline.sh`: 카테고리별 실험 자동화 쉘 스크립트.
- `source/results/`: 재현 결과 CSV 파일들.
- `markdown/`: 상세 분석 보고서 및 결과 테이블.
- `source/patchcore_colab.ipynb`: 원본 Colab 실험 노트.
