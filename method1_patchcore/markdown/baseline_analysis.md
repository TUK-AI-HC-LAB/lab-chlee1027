# PatchCore Baseline 재현 및 프로파일링 분석 (MVTec AD 완결)

> 재현 실행: 2026-05-06 ~ 2026-05-11 / 프로파일링: 2026-05-29 (Colab T4 GPU)
> 논문: Roth et al. 2022 — `method1_patchcore/paper/roth2022.pdf`
> 상세 결과 테이블: `method1_patchcore/markdown/baseline_full_table.md`
> 원시 데이터: AUROC(`.../results/baseline_*.csv`), Profile(`.../results/baseline_profile_results.csv`)

## 1. 개요 및 목적
본 보고서는 PatchCore baseline의 **성능(AUROC)** 재현과 **효율성(Runtime/Memory)** 프로파일링을 통합하여 정리합니다. 논문 수치 재현을 통해 베이스라인의 신뢰도를 확보하는 동시에, 연산 단계별 병목 지점을 정량적으로 진단하여 실시간 가속 전략(FAISS 도입 등)의 객관적 근거를 수립합니다.

## 2. 실험 환경 및 설정
- **환경**: Colab T4 GPU (Python 3.12, torch 2.x, faiss-cpu 1.13.2)
- **모델 설정**: WideResNet-50 (layers 2+3), Coreset p=0.1 (10%), Seed 0
- **추론 설정**: Resize 256, Crop 224, Batch Size 1

## 3. 성능 재현 결과 (15개 전 카테고리)
- **I-AUROC 평균**: 0.992 (논문 0.991)
- **P-AUROC 평균**: 0.982 (논문 0.981)
모든 카테고리에서 논문 수치 대비 동등 이상의 성능을 보이며 성공적으로 재현되었습니다. (상세 내역은 `baseline_full_table.md` 참조)

## 4. 연산 단계별 프로파일링 분석 (Efficiency Analysis)

### 4.1. kNN Search 병목 규명
*   **지배적 지연 시간**: Exact L2 kNN 탐색은 전체 추론 시간의 **평균 90.8%**를 점유하는 압도적인 병목 구간입니다.
*   **스케일링 제약**: `hazelnut` 등 대형 카테고리에서 지연 시간이 **868.22 ms/img**에 육박하여, 실시간 감지 임계 한도($\le 50$ms)를 크게 초과함이 확인되었습니다.
*   **결론**: 성능(AUROC)은 완벽하지만, 탐색 지연이 메모리 뱅크 크기에 선형 비례하여 팽창하므로 실시간 배포를 위한 인덱스 가속이 필수적입니다.

### 4.2. Memory Bank Build 및 기타 단계
*   **학습 단계**: Coreset Subsampling 과정에서 `hazelnut` 기준 최대 **1.40 GB**의 메모리 스파이크와 **79.04 s**의 빌드 지연이 계측되었습니다.
*   **추능 단계**: Feature Extraction(약 45ms), Post-processing(약 3ms)은 안정적인 균등성을 보이며 런타임 영향력이 낮습니다.

## 5. 주요 관찰 및 인사이트
- **Pill (-0.011):** 10% 샘플링 시 미세 성능 하락 관찰. 추가 실험을 통해 **1% 샘플링 시 최고 성능(0.980)**을 내는 '샘플링의 역설'을 확인하였습니다.
- **성능 vs 속도 트레이드오프**: PatchCore의 고성능은 거대한 메모리 뱅크와 전수 탐색(Exact Search)에 기반하고 있으나, 이는 실시간성 확보의 아킬레스건으로 작용합니다.
- **최적화 타겟**: 가속화를 위해 Backbone 네트워크 개선보다는 **kNN Search 단계 자체를 선형 이하(Sub-linear) 시간으로 처리하는 ANN(Approximate Nearest Neighbor) 인덱스 도입**이 최우선 과제입니다.

## 6. 결론 및 향후 가속 방향 (Active Research)
본 진단을 기점으로 PatchCore의 한계를 명확히 규명하였으며, 이를 개선하기 위한 차세대 2단계 로드맵을 추진합니다.
1.  **FAISS 가속 인덱스 탑재**: HNSW, IVF, PQ 등 다양한 인덱스 알고리즘을 이식하여 탐색 속도 가속화.
2.  **파레토 프론티어 규명**: AUROC 하락을 1% 이내로 방어하면서 Latency를 5배 이상(100ms 미만) 단축시키는 최적의 Trade-off 지점 실증.
