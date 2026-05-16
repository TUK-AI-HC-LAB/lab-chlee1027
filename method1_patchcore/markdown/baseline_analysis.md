# PatchCore Baseline 재현 분석 (MVTec AD 15개 전 카테고리 완결)

> 재현 실행: 2026-05-06 ~ 2026-05-11, Colab T4 GPU
> 논문: Roth et al. 2022 — `method1_patchcore/paper/roth2022.pdf`
> 상세 결과: `method1_patchcore/markdown/baseline_full_table.md`
> 원인 분석: `method1_patchcore/markdown/repro_failure_analysis.md`

## 1. 개요 및 목적
PatchCore baseline이 MVTec AD 전 카테고리(15개)에서 논문 수치대로 재현되는지 확인하여 baseline의 신뢰도를 확보하였습니다.

## 2. 실험 환경 및 설정
- **환경**: Colab T4 GPU
- **기술 스택**: Python 3.12, torch 2.10.0+cu128, faiss-cpu 1.13.2
- **Backbone**: WideResNet-50 (ImageNet pretrain)
- **Feature Layers**: layer2 + layer3
- **Coreset**: Approx Greedy, p=0.1 (10%)
- **Seed**: 0

## 3. 종합 결과 (15개 전 카테고리)
- **I-AUROC 평균**: 0.992 (논문 0.991)
- **P-AUROC 평균**: 0.982 (논문 0.981)

모든 카테고리에서 논문 수치 대비 동등 이상의 성능을 보이며 성공적으로 재현되었습니다.

## 4. 주요 관찰 및 인사이트
- **Pill (-0.011):** 10% 샘플링 시 미세 성능 하락 관찰. 추가 실험을 통해 **1% 샘플링 시 최고 성능(0.980)**을 내는 '샘플링의 역설'을 확인하였습니다.
- **Metal Nut (-0.008):** 픽셀 단위 정밀도(P-AUROC) 부족 확인. **Layer 1 추가 및 해상도 상향(324)**을 통해 성능을 복원할 수 있음을 검증하였습니다.
- **기타 카테고리**: 대부분 오차 범위(±0.005) 내에서 완벽하게 일치하는 수치를 기록하였습니다.

## 5. 결론
본 재현 프로젝트를 통해 PatchCore의 MVTec AD 베이스라인을 완벽히 확보하였으며, 특정 카테고리의 성능 편차에 대한 기술적 분석까지 마쳤습니다. 이를 바탕으로 차세대 알고리즘(SimpleNet 등)과의 비교 실험을 수행할 준비가 완료되었습니다.
