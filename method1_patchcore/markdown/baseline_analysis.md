# PatchCore baseline 재현 분석 (bottle, leather)

> 재현 실행: 2026-05-06, Colab T4 GPU
> 논문: Roth et al. 2022 — `method1_patchcore/paper/roth2022.pdf`
> 요약 노트: `method1_patchcore/markdown/roth2022_summary.md`

## 문제 / 동기

PatchCore baseline이 **자기 환경에서도 논문 수치대로 재현되는지** 확인. 이후 ablation·후속 연구 비교의 기준점이 필요하므로 가장 먼저 baseline의 신뢰도를 확보해야 한다.

## 시도

**환경**
- Colab T4 GPU
- Python 3.12, torch 2.10.0+cu128, faiss-cpu 1.13.2
- upstream: amazon-science/patchcore-inspection (clone)

**설정** (논문 PatchCore-10% 기본)
- backbone: WideResNet-50 (ImageNet pretrain)
- feature layers: layer2 + layer3
- pretrain_embed_dim 1024, target_embed_dim 1024
- coreset: approx greedy, p=0.1 (10%)
- anomaly scoring: NN=1, patchsize=3
- 입력: resize 256 → center crop 224
- seed: 0

**실행 파일**
- 셸: `method1_patchcore/source/run_baseline.sh` (CATEGORY 환경변수)
- 노트북: `method1_patchcore/source/patchcore_colab.ipynb` (Colab 원본)
- 수정: `image_transform()` 내 `dataset.transform_std/_mean` 접근을 ImageNet 표준값으로 하드코딩 (시각화 단계에만 영향)

## 결과

**bottle** (`method1_patchcore/source/results/baseline_bottle_20260506.csv`)
- Image-AUROC: 1.000 (논문 1.000)
- Full Pixel-AUROC: 0.985 (논문 P-AUROC 0.986)
- Anomaly Pixel-AUROC: 0.980
- 학습+평가 시간: ~40초 (T4)

**leather** (`method1_patchcore/source/results/baseline_leather_20260506.csv`)
- Image-AUROC: 1.000 (논문 1.000)
- Full Pixel-AUROC: 0.993 (논문 P-AUROC 0.990)
- Anomaly Pixel-AUROC: 0.990
- 학습+평가 시간: ~50초 (T4)

→ 4개 지표 전부 논문값과 ±0.005 이내. **재현 성공**.

## 관찰

- bottle, leather 모두 **MVTec AD에서 PatchCore가 매우 강한** 카테고리. Image-level은 1.000으로 saturating.
- Pixel-level도 0.98~0.99로 거의 한계 — 추가 개선 여지가 작은 영역.
- T4 무료 환경에서도 카테고리당 1분 이내 실행. 비용 부담 없음.
- Coreset subsampling 단계가 가장 시간을 많이 씀 (memory bank 16k~19k 항목 → 10%로 압축).

