# Deng et al. 2022 — Anomaly Detection via Reverse Distillation from One-Class Embedding (RD)

> Hanqiu Deng, Xingyu Li. CVPR 2022.
> 원문 PDF: `method3_RD/paper/Reverse_Distillation_CVPR2022.pdf`

## 한 줄 요약

기존 Knowledge Distillation(KD) 기반 이상 탐지가 Teacher·Student를 **같은 구조**로 두어 정상에서도 student가 teacher를 잘 따라가는 한계를 해결. Teacher는 **Encoder**, Student는 **Decoder**로 두고 그 사이를 **One-Class Bottleneck Embedding(OCBE)** 으로 압축한다. Student Decoder가 정상 데이터의 Teacher feature를 잘 복원하지만 이상에선 복원 실패 → 복원 오차를 anomaly score로. MVTec AD 평균 I-AUROC 98.5%, 추론 0.31s/img.

## 문제 / 동기

- **Cold-start anomaly detection** 동일 — 정상만 있고 비정상은 거의 없는 산업 환경
- 기존 KD 기반 anomaly detection의 한계
  - **같은 구조 Teacher·Student**: ImageNet으로 pretrain된 Teacher와 동일 구조의 Student를 학습. 그런데 구조가 같으면 정상뿐 아니라 **이상 영역에서도 student가 teacher를 따라잡아 버려** anomaly signal이 약해짐
  - **단일 레벨 feature**: 깊은 layer 하나만 쓰면 다양한 크기·종류의 결함을 못 잡음
- 기존 Embedding 기반(PatchCore, PaDiM)의 한계
  - memory bank 의존 → 추론 비용·메모리 부담
- 목표: **구조 비대칭으로 student가 정상에만 fit하도록 강제하고**, **multi-level feature로 다양한 결함 커버**, **추론은 가볍게**

## 핵심 아이디어 3가지

### 1. Reverse Distillation — Teacher=Encoder, Student=Decoder

- **Conventional KD**: Teacher(Encoder) → Student(Encoder) — 같은 방향, 같은 구조
- **Reverse Distillation**: Teacher(Encoder) → OCBE(bottleneck) → Student(Decoder) — **방향과 구조가 모두 다름**
- Student Decoder는 OCBE로 압축된 신호로부터 Teacher Encoder의 feature를 **역으로 복원**하도록 학습
- 정상만 학습했기에 정상 feature는 잘 복원되지만, 이상 feature는 복원 실패 → **복원 오차가 anomaly signal**
- 구조 비대칭 덕분에 student가 이상까지 따라잡지 못함 (KD-AD의 핵심 결함 해결)

### 2. One-Class Bottleneck Embedding (OCBE)

- Teacher와 Student 사이의 **병목**. 두 하위 모듈로 구성:
  - **MFF (Multi-scale Feature Fusion)**: Teacher의 low~high level feature를 결합 — 다양한 크기·종류의 결함 커버
  - **OCE (One-Class Embedding)**: 결합된 feature를 압축 → 정상 패턴의 정수만 남기고 **이상치 노이즈를 차단하는 필터** 역할
- 결과: Student가 받는 입력은 "정상의 본질만 남은 압축 표현" → 정상은 잘 복원, 이상은 압축 단계에서부터 정보 손실로 복원 실패

### 3. Multi-level Cosine 거리로 채점

- Teacher의 각 layer feature $f_T^k$ vs Student가 복원한 feature $f_S^k$ 간 **cosine similarity**를 계산
- $1 - \cos(f_T^k, f_S^k)$ 가 layer-level anomaly map
- 여러 layer의 map을 합쳐 최종 pixel-level / image-level score 산출
- Cosine 거리는 magnitude에 둔감 → 백본 출력 스케일 변동에 robust

## 학습 / 추론 흐름

학습 (4-component):
```
image → Teacher Encoder → [feature f_T^k] ┐
                                          ├→ OCBE (MFF + OCE) → Student Decoder → [f_S^k]
                                          ┘                                          ↓
                                                              loss = 1 - cos(f_T^k, f_S^k)
```

- **Teacher Encoder는 고정** (ImageNet pretrain WRN-50/ResNet50 등)
- **OCBE·Student Decoder만 학습**

추론 (동일 path, score 계산만 다름):
```
image → Teacher Encoder → OCBE → Student Decoder
          ↓                              ↓
       f_T^k       1 - cos(f_T^k, f_S^k) per layer
                              ↓
                          anomaly map / score
```

- 추가 모듈 없이 단일 forward — memory bank 검색 불필요

## 주요 결과 (논문 발췌)

- MVTec AD 평균 **Image-AUROC 98.5%**
- MVTec AD 평균 **Pixel-AUROC 97.8%**
- **PRO 93.9%** (Per-Region Overlap)
- 추론 속도 **0.31s/img**, 메모리 **352MB**
- 다양한 카테고리에서 안정적 성능 (특정 카테고리에 의존적이지 않음)

## PatchCore·SimpleNet과의 차별점

| 항목 | PatchCore (method1) | SimpleNet (method2) | Reverse Distillation (method3) |
|---|---|---|---|
| 핵심 메커니즘 | Memory bank + NN | Discriminator (GAN-like) | Encoder-Decoder 복원 오차 |
| 학습 필요? | ❌ (memory bank만 구축) | ✅ (Adaptor + Discriminator) | ✅ (Student Decoder + OCBE) |
| 구조 대칭성 | n/a | n/a | **비대칭** (Encoder ↔ Decoder) |
| 이상 신호 | NN 거리 | Discriminator 점수 | feature 복원 cosine 오차 |
| 합성 결함 | 사용 안 함 | feature-space에서 Gaussian noise로 합성 | 사용 안 함 |
| 추론 메모리 | memory bank (수만 patch) | MLP 가중치 | Decoder 가중치 (~352MB) |
| 추론 속도 (논문) | NN 검색 비용 | ~77 FPS | ~0.31s/img |
| MVTec AD 평균 I-AUROC | 99.1~99.6% | 99.6% | 98.5% |

→ RD는 **"왜 KD-AD가 안 됐는가"** 에 대한 구조적 답(비대칭 + bottleneck). PatchCore의 "memory 의존"과 SimpleNet의 "합성 의존" 모두를 피하면서도 학습 기반.

## 본 재현 진행 상황

### MVTec AD 14/15 재현 진행 (2026-05-21, Colab T4)

upstream **[hq-deng/RD4AD](https://github.com/hq-deng/RD4AD)** (공식 구현체) 사용. `test.py` pandas 호환 수정 + `main_single.py` 단일 카테고리 실행 래퍼. 학습 설정: img 256, batch 16, lr 0.005, epochs 200.

**결과 요약** (전체 표: [`baseline_full_table.md`](baseline_full_table.md))

| 지표 | 재현 평균(14개) | 논문 |
|---|---|---|
| I-AUROC | **0.987** | 0.985 |
| Full P-AUROC | **0.978** | 0.977 |

- 14/15 완료 (잔여: hazelnut). grid·leather·metal_nut·wood I-AUROC 1.000
- 재현 평균이 원논문 보고치(98.5/97.8)와 거의 완벽히 일치 (재현 성공)
- 강점: wood·screw 등 텍스처 픽셀 정밀도 / 약점: cable·transistor (다양 패턴)

### 다음 단계

1. ~~upstream 확정~~ → **hq-deng/RD4AD** 확정
2. ~~baseline 실행~~ → 14/15 완료, hazelnut 잔여
3. ~~3-way 비교 노트 작성~~ → **완료** ([`rd_vs_patchcore_simplenet.md`](rd_vs_patchcore_simplenet.md))
4. ~~paper 컬럼 원논문 기준 검증~~ → **완료** (Table 1·2 직접 전사, ΔI +0.002)
5. hazelnut 완료 후 15/15 평균 확정

> 실행 가이드: [`../source/README.md`](../source/README.md)
> 재현 분석: [`baseline_analysis.md`](baseline_analysis.md)
