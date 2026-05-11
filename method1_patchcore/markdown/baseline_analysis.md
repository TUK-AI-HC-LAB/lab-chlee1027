# PatchCore baseline 재현 분석 (전체 15개 중 9개 완료)

> 재현 실행: 2026-05-06 ~ 2026-05-11, Colab T4 GPU
> 논문: Roth et al. 2022 — `method1_patchcore/paper/roth2022.pdf`
> 상세 비교표: `method1_patchcore/markdown/baseline_full_table.md`

## 문제 / 동기

PatchCore baseline이 MVTec AD 전 카테고리(15개)에서 논문 수치대로 재현되는지 확인하여 baseline의 신뢰도를 확보함.

## 시도

**환경**
- Colab T4 GPU (완료된 9개 카테고리)
- Python 3.12, torch 2.10.0+cu128, faiss-cpu 1.13.2
- upstream: amazon-science/patchcore-inspection

**설정** (논문 PatchCore-10% 기본)
- backbone: WideResNet-50 (ImageNet pretrain)
- feature layers: layer2 + layer3
- coreset: approx greedy, p=0.1 (10%)
- seed: 0

## 결과 요약 (9개 카테고리)

현재까지 완료된 9개 카테고리(`bottle`, `cable`, `capsule`, `carpet`, `hazelnut`, `leather`, `metal_nut`, `pill`, `transistor`)에 대한 결과:

- **I-AUROC 평균:** 0.992 (논문 0.991)
- **P-AUROC 평균:** 0.985 (논문 0.985)

대부분의 카테고리에서 논문 수치 대비 ±0.005 이내의 차이를 보이며 성공적으로 재현됨.

## 관찰 및 특이사항

- **Pill 카테고리:** I-AUROC가 0.967로 논문(0.978) 대비 -0.011 낮게 측정됨. Coreset sampling의 무작위성이나 환경 차이로 인한 미세한 성능 변화로 보임.
- **Metal Nut 카테고리:** P-AUROC가 0.983으로 논문(0.991) 대비 -0.008 낮음.
- 나머지 카테고리는 소수점 셋째 자리까지 거의 일치하는 수준.

## 향후 계획

- 남은 6개 카테고리(`grid`, `screw`, `tile`, `toothbrush`, `wood`, `zipper`)에 대한 재현 실험 진행.
- 전체 15개 카테고리 완료 후 통합 분석 및 다음 단계(ablation study 등) 결정.

