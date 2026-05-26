# Dinomaly Baseline 재현 분석 (MVTec AD 15개 전 카테고리 완결)

> 재현 실행: 2026-05-25, Colab T4 GPU
> 논문: Guo et al. 2025 — `method4_Dinomaly/paper/Dinomaly_CVPR2025.pdf`
> 논문 요약: `method4_Dinomaly/markdown/dinomaly_summary.md`
> 상세 결과: `method4_Dinomaly/markdown/baseline_full_table.md`
> 4-way 비교: `method4_Dinomaly/markdown/4-way_comparison_framework.md`

## 1. 개요 및 목적
Dinomaly (CVPR 2025) baseline을 MVTec AD에서 재현하여, 기존 3개 Method(PatchCore, SimpleNet, RD)를 뛰어넘는 새로운 성능 기준선을 확보한다. 특히 단일 통합 모델(Multi-class Unified)로서의 효율성과 성능을 동시에 검증하는 데 목적이 있다. 15개 전 카테고리 재현 완료.

## 2. 실험 환경 및 설정
- **환경**: Colab T4 GPU
- **기술 스택**: Python 3.12, torch 2.x
- **upstream**: [guojiajeremy/Dinomaly](https://github.com/guojiajeremy/Dinomaly) (공식 구현체)
*   **Backbone (Encoder)**: DINOv2 (ViT-Base/14, Frozen)
*   **Architecture**: MLP Bottleneck (Dropout 0.2) + ViT Decoder (Linear Attention)
- **학습 설정**: Resize 448 / Crop 392, Batch 16, LR 2e-3, 10,000 Iterations
- **수정**: `utils.py` pandas 호환(`pd.concat`), CUDA 디바이스 자동화, 카테고리 필터링 로직 (상세: `../source/README.md`)

## 3. 종합 결과 (15개 전 카테고리)
- **I-AUROC 평균**: 0.9962 (논문 0.996)
- **Full P-AUROC 평균**: 0.9832 (논문 0.984)

김준아 학생의 선행 재현 결과(0.9962)와 **소수점 4자리까지 완벽히 일치**함을 확인하였으며, 논문 보고치와 비교해도 ΔI +0.000, ΔP -0.001 수준의 높은 정밀도로 재현에 성공했다. 총 15개 중 9개 카테고리에서 I-AUROC 1.000을 달성했다.

## 4. 주요 관찰 및 인사이트
- **MUAD의 혁신적 효율성:** 기존 Method(M1~M3)가 15개의 독립된 모델을 필요로 했던 것과 달리, Dinomaly는 **단 하나의 모델(Single Weight)**로 15개 전체 카테고리에서 최고 성능을 달성. 이는 모델 관리 및 실무 배포 측면에서 비약적인 진보임.
- **DINOv2 특징의 변별력:** 강력한 사전학습 특징을 활용하여 `bottle`, `leather`, `cable`, `hazelnut` 등 다양한 카테고리에서 완벽한 탐지 성능을 보여줌.
- **구조적 강점 (Linear Attention):** Softmax Attention의 집중 현상을 억제하여 정보를 분산 복원하게 함으로써, 이상치까지 복원해버리는 identity mapping 문제를 효과적으로 차단함.
- **상대적 약점 (미세 결함):** `capsule`(0.979) 및 `screw`(0.985)에서 타 카테고리 대비 소폭 낮은 성능을 보임. 이는 "Loose Reconstruction" 방식이 픽셀 단위의 극도로 미세한 특징 변화를 '정상 복원 오차' 범위로 간주할 수 있는 구조적 특성에 기인한 것으로 분석됨.
- **4-way 상보성:** 이미지 탐지 및 통합 효율성은 Dinomaly가 압도적이며, 텍스처 정밀도는 RD, 저해상도 고효율은 PatchCore가 각각의 강점을 유지함 (상세: `4-way_comparison_framework.md`).

## 5. 결론
Dinomaly baseline 재현을 통해 MVTec AD 벤치마크의 새로운 SOTA(Mean I-AUROC 0.9962)를 확정했다. 특히 Multi-class 통합 모델 하나로 개별 학습 모델들을 압도하는 성능을 냄으로써, 향후 연구 방향이 '통합 모델 기반의 고효율 이상치 탐지'로 전환될 수 있음을 시사한다. 이로써 4개 Method에 대한 모든 재현 및 분석 과정을 성공적으로 완결했다.
