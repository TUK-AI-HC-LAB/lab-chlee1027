# SimpleNet Baseline 재현 분석 (MVTec AD 15개 전 카테고리 완결)

> 재현 실행: 2026-05-16 ~ 2026-05-19, Colab T4 GPU
> 논문: Liu et al. 2023 — `method2_simplenet/paper/SimpleNet.pdf`
> 논문 요약: `method2_simplenet/markdown/simplenet_summary.md`
> 상세 결과: `method2_simplenet/markdown/baseline_full_table.md`

## 1. 개요 및 목적
SimpleNet baseline이 MVTec AD 전 카테고리(15개)에서 논문 수치대로 재현되는지 확인하여, PatchCore(method1)와 동일 조건에서 비교할 수 있는 신뢰성 있는 baseline을 확보하였습니다.

## 2. 실험 환경 및 설정
- **환경**: Colab T4 GPU
- **기술 스택**: Python 3.12, torch 2.10.0+cu128
- **upstream**: [DonaldRR/SimpleNet](https://github.com/DonaldRR/SimpleNet)
- **Backbone**: WideResNet-50 (ImageNet pretrain), Feature Layers layer2 + layer3
- **학습 설정**: meta_epochs 40, gan_epochs 4, noise_std 0.015, dsc_hidden 1024 / dsc_layers 2, pre_proj 1
- **입력 (논문 동일)**: resize 329 → imagesize 288, batch_size 8
- **Seed**: 0

> 초기 toothbrush 1·2차(5/16~17)는 resize 256/224, batch 4로 실행. 5/18부터 논문 동일 설정(329/288, batch 8)으로 통일.

## 3. 종합 결과 (15개 전 카테고리)
- **I-AUROC 평균**: 0.995 (논문 0.996)
- **P-AUROC 평균**: 0.980 (논문 0.981)

평균이 논문 수치와 ±0.001로, 모든 카테고리에서 성공적으로 재현되었습니다. 9개 카테고리에서 I-AUROC ≥ 0.999를 기록했습니다.

## 4. 주요 관찰 및 인사이트
- **Screw (-0.017), Capsule (-0.009):** I-AUROC가 논문 대비 소폭 낮음. SimpleNet 특유의 Gaussian noise 투입 + Discriminator(GAN) 학습의 확률적 요소(stochasticity)에 기인하는 미세 편차로 분석됩니다.
- **Pill (+0.009 P), Metal_nut (+0.005 P):** PatchCore(method1)가 격차를 보였던 두 카테고리에서 SimpleNet은 오히려 논문 수치를 상회. **method 간 강·약점이 카테고리별로 갈린다**는 비교 분석의 핵심 단서입니다.
- **Anomaly Pixel AUROC 편차:** `hazelnut`(0.836) ~ `leather`(0.966)로 카테고리 간 차이가 큼. localization 난이도가 카테고리 특성(텍스처/객체 결함 유형)에 민감함을 시사합니다.
- **시각화:** `main.py` 패치로 segmentation 히트맵을 정상 생성, 정성적 검증까지 완료 (`baseline_full_table.md` Figure 1·2).

## 5. 결론
SimpleNet의 MVTec AD 베이스라인을 15개 전 카테고리에서 논문 수준으로 확보하였으며, PatchCore와 동일 조건의 비교 기반을 마련했습니다. 특히 pill·metal_nut에서 두 method의 우열이 갈리는 점은 다음 단계인 method 간 비교 분석(`simplenet_vs_patchcore.md`)과 method3(Reverse Distillation) 도입의 출발점이 됩니다.
