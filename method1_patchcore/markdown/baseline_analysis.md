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

## 의문 / 추가 확인 필요

1. **dataset attribute 부재 이유**: upstream의 `image_transform()` 이 `dataset.transform_std/_mean` 을 참조하는데 실제 dataset 클래스에 그 속성이 없음. upstream 코드 버전과 환경(faiss 버전, torch 버전 등)에 따른 차이인지, 아니면 단순한 upstream 버그인지 확인 필요. → 다음 주에 upstream 최신 commit 따라가서 비교.
2. **포화된 지표**: bottle, leather처럼 거의 1.000 나오는 카테고리에선 baseline-vs-개선법 비교가 어렵다. 의미있는 비교를 하려면 어려운 카테고리(cable, transistor 등)도 봐야 함.
3. **seed 의존성**: seed 0만 돌렸음. PatchCore는 NN 기반이라 randomness 영향이 작을 것으로 보이지만 (coreset의 random init 정도), 1~2개 다른 seed로 확인이 필요.

## 다음

- [ ] coreset ablation: p=0.01, 0.25 비교 (bottle, leather)
- [ ] 어려운 카테고리 추가: cable, transistor 최소 1개씩
- [ ] PatchCore 후속 논문 1편 골라서 다음 method 후보로 — PNI / EfficientAD / DSR 등
- [ ] (선택) seed 변동 확인 — seed 0/1/2
