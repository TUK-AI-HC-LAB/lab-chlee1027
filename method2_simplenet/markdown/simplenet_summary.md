# Liu et al. 2023 — SimpleNet: A Simple Network for Image Anomaly Detection and Localization

## Paper Metadata

| 항목 | 내용 |
|---|---|
| 제목 | SimpleNet: A Simple Network for Image Anomaly Detection and Localization |
| 저자 | Zhikang Liu, Yiming Zhou, Yuansheng Xu, Zilei Wang |
| 학회/저널 | CVPR |
| 연도 | 2023 |
| 논문 링크 | [CVPR 2023 Open Access](https://openaccess.thecvf.com/content/CVPR2023/html/Liu_SimpleNet_A_Simple_Network_for_Image_Anomaly_Detection_and_CVPR_2023_paper.html) |
| GitHub / 공식 코드 | [DonaldRR/SimpleNet](https://github.com/DonaldRR/SimpleNet) |
| 조사 이유 | 메모리 뱅크가 없는 학습 기반 이상 탐지 모델로서, 가상 이상치 합성 및 판별기 구조 분석과 재현을 위함 |

> 원문 PDF: `method2_simplenet/paper/SimpleNet.pdf`

## 한 줄 요약

ImageNet 사전학습 백본의 patch feature를 **단일 FC layer(Adaptor)** 로 산업 도메인에 투영하고, 정상 feature에 **Gaussian noise를 더해 가짜 이상 feature를 생성**, 둘을 **2-layer MLP(Discriminator)** 로 분류한다. memory bank 없이 학습 기반으로 MVTec AD 99.6% I-AUROC, 77 FPS 달성.

## 문제 / 동기

- **Cold-start anomaly detection** 동일 — 정상만 있고 비정상은 거의 없는 산업 환경
- 기존 3가지 접근의 한계
  - **Reconstruction-based**: 정상만으로 학습해 비정상은 못 복원할 거라 가정하지만, 실제론 비정상 영역도 잘 복원해버림 (generalization gap)
  - **Synthesizing-based** (DRAEM 등): 이미지 공간에 가짜 결함을 합성. 합성된 결함이 실제 결함 분포와 어긋남
  - **Embedding-based** (PatchCore, PaDiM): ImageNet pretrain feature를 그대로 사용 — 산업 이미지와의 **domain bias**로 성능 제한 + memory bank로 인한 메모리·시간 비용
- 목표: **domain bias 줄이고, 학습 가능하면서, 추론은 가볍게**

## 핵심 아이디어 3가지

### 1. Feature Adaptor — 산업 도메인 투영

- pretrained 백본(WRN-50)에서 mid-level patch feature 추출 (PatchCore와 동일 출발점)
- **단일 FC layer**로 ImageNet feature를 타겟 도메인으로 projection
- **얕은 어댑터로도 충분** — 핵심은 "쓸 만한 feature를 어떻게 만드느냐"가 아니라 "domain bias를 어떻게 떼느냐"
- PatchCore는 raw feature를 memory bank에 저장, SimpleNet은 adapted feature를 사용

### 2. Feature-space Anomaly Synthesis — 가짜 이상은 feature에서

- 어댑터 통과 후 정상 feature $f$ 에 가우시안 노이즈 $\mathcal{N}(\mu, \sigma^2)$ 를 더해 가상의 이상 feature $f' = f + \epsilon$ 생성
- **이미지 공간이 아니라 feature 공간에서** 합성 — DRAEM류의 "실제 결함 분포와 어긋남" 문제를 회피
- 학습 시에만 사용, **추론 시엔 제거** (단일 stream으로 빠르게 동작)

### 3. Discriminator — 학습 기반 채점

- **2-layer MLP**가 정상 feature(양성) vs 합성 이상 feature(음성)를 분류
- Loss: **Truncated L1** — 분류 경계에 너무 가까운 정상도, 너무 먼 이상도 양쪽 다 무시 (overfitting 방지)
- 추론 시 Discriminator 출력 = anomaly score, max score 위치 = 결함 추정 위치

## 학습 / 추론 흐름

학습 (4-component):
```
image → Feature Extractor → Feature Adaptor → [Anomaly Feature Generator] → Discriminator → loss
                                              (정상→가짜 이상 생성)
```

추론 (3-component, Generator 제거):
```
image → Feature Extractor → Feature Adaptor → Discriminator → anomaly score
```

- 백본: 보통 **WideResNet-50** (PatchCore와 동일)
- Adaptor·Discriminator만 학습되고 백본은 고정
- 추론 단일 stream — memory bank 조회/NN 검색이 없어 빠름

## 주요 결과 (논문 발췌)

- MVTec AD 평균 **Image-AUROC 99.6%** (당시 SOTA, 직전 baseline 대비 **error 55.5% 감소**)
- Pixel-level localization도 SOTA급
- **77 FPS** (RTX 3080 Ti) — embedding-based 대비 ~50 FPS 빠름
- 모듈이 단순(FC, MLP, Gaussian noise)해 구현·튜닝이 쉬움

## PatchCore와의 차별점

| 항목 | PatchCore (method1) | SimpleNet (method2) |
|---|---|---|
| 학습 필요? | ❌ (memory bank만 구축) | ✅ (Adaptor + Discriminator 학습) |
| domain bias 대응 | 없음 (raw ImageNet feature) | Feature Adaptor로 투영 |
| 이상 신호 | NN 거리 (정상 분포 외곽) | Discriminator 점수 (학습된 판별 경계) |
| 추론 메모리 | memory bank (수만 개 patch) | MLP 가중치만 |
| 합성 결함 | 사용 안 함 | feature-space에서 Gaussian noise로 합성 |
| 추론 속도 | NN 검색 비용 | 단일 forward pass (~77 FPS) |
| MVTec AD 평균 I-AUROC | 99.1~99.6% | 99.6% |

→ SimpleNet은 **PatchCore의 "raw feature + memory bank" 한계**(domain bias, 메모리)에 대한 학습 기반 응답.

## 본 재현 진행 상황

### MVTec AD 전 카테고리(15/15) 재현 완료 (2026-05-16 ~ 19, Colab T4)

upstream **[DonaldRR/SimpleNet](https://github.com/DonaldRR/SimpleNet)** 사용. 5/16 toothbrush 1차 실행 → 시각화 미생성 이슈 발견 → 5/17 `main.py` 패치 + 재실행 → 5/18~19 논문 동일 파라미터로 전 카테고리 확장. 자세한 수정 내역은 [`../source/README.md`](../source/README.md) "수정 내역" 섹션.

**수정 3건**
1. `metrics.py` — pandas 2.0+ 호환 (`df.append()` → `df.loc[len(df)] = ...`)
2. `main.py` — 주석 처리된 `test()` 호출 활성화 + `train()` 완료 후 자동 시각화
3. `simplenet_colab.ipynb` — 위 패치들을 자동 실행 셀 + 결과 이미지 수직 나열 출력 셀 추가

**하이퍼파라미터** (5/18~19 전 카테고리 — 논문 동일 설정)

| 항목 | 값 |
|---|---|
| backbone | WideResNet-50 |
| feature layers | layer2 + layer3 |
| pretrain / target embed dim | 1536 / 1536 |
| patchsize | 3 |
| meta_epochs | 40 |
| gan_epochs | 4 |
| noise_std (Generator) | 0.015 |
| dsc_hidden / dsc_layers | 1024 / 2 |
| dsc_margin | 0.5 |
| pre_proj | 1 |
| batch_size | 8 |
| **resize / imagesize** | **329 / 288 (논문 설정)** |
| seed | 0 |

> 초기 toothbrush 1·2차(5/16~17)는 resize 256/224, batch 4로 실행. 5/18부터 논문 동일 설정(329/288, batch 8)으로 통일.

**결과 요약** (전체 표: [`baseline_full_table.md`](baseline_full_table.md))

| 지표 | 재현 평균 | 논문 평균 | Δ |
|---|---|---|---|
| I-AUROC | **0.995** | 0.996 | -0.001 |
| Full P-AUROC | **0.980** | 0.981 | -0.001 |

- 15개 전 카테고리 모두 Done, 평균이 논문 수치와 ±0.001 — **재현 성공**
- 9개 카테고리에서 I-AUROC ≥ 0.999 (bottle·leather·metal_nut·transistor·wood·zipper 등 1.000)

**관찰**
- 평균 I-AUROC 0.995로 논문(0.996)과 거의 일치 — SimpleNet baseline 신뢰성 확보
- 편차가 큰 항목: `screw`(I -0.017), `capsule`(I -0.009) — Gaussian noise 투입 + Discriminator(GAN) 학습의 확률적 요소(stochasticity)에 기인하는 것으로 분석
- Anomaly Pixel AUROC는 카테고리 편차가 큼(`hazelnut` 0.836 ~ `leather` 0.966) — localization 난이도가 카테고리 특성에 민감
- PatchCore가 격차를 보였던 `pill`(P +0.009), `metal_nut`(P +0.005)에서 SimpleNet은 오히려 논문 상회 — method 간 비교 분석 흥미로운 지점

### 다음 단계

1. ~~카테고리 확장 (15개)~~ → **완료**
2. ~~노트북 → 셸 스크립트화 (`run_baseline.sh`, CATEGORY 환경변수)~~ → **완료** ([`../source/run_baseline.sh`](../source/run_baseline.sh))
3. PatchCore baseline과 직접 비교 — 특히 PatchCore가 격차를 보였던 pill, metal_nut에서 SimpleNet 우위 확인
4. ~~비교 분석 노트 작성 — `simplenet_vs_patchcore.md`~~ → **완료** ([`simplenet_vs_patchcore.md`](simplenet_vs_patchcore.md))

> 실행 가이드: [`../source/README.md`](../source/README.md)
> 노트북: [`../source/simplenet_colab.ipynb`](../source/simplenet_colab.ipynb)
> 통합 결과: [`baseline_full_table.md`](baseline_full_table.md)
