# Guo et al. 2025 — Dinomaly: The Less Is More Philosophy in Multi-Class Unsupervised Anomaly Detection

> Jia Guo, Shuai Lu, Weihang Zhang, Fang Chen, Huiqi Li, Hongen Liao. CVPR 2025.
> 원문 PDF: `method4_Dinomaly/paper/Dinomaly_CVPR2025.pdf`
> arXiv: [2405.14325](https://arxiv.org/abs/2405.14325)

## 한 줄 요약

DINOv2 사전학습 ViT를 Encoder로, **Dropout 병목 + Linear Attention + Loose Reconstruction**이라는 세 가지 "덜어내는" 설계로 identity mapping을 차단하는 순수 Transformer 기반 복원형 프레임워크. **Multi-class 통합 모델 하나로** MVTec AD I-AUROC 99.6%를 달성하여 기존 class-separated SOTA까지 돌파.

## 문제 / 동기

- **Cold-start anomaly detection** 동일 — 정상만 있고 비정상은 거의 없는 산업 환경
- **Multi-class UAD의 핵심 문제 — Identity Mapping:**
  - 기존 방식(UniAD 등)은 클래스별 모델을 따로 학습. 산업 현장에서는 수십~수백 클래스를 한 모델로 커버해야 실용적
  - 복원(reconstruction) 기반 방법을 multi-class로 확장하면, 정상 패턴이 너무 다양해져 네트워크가 **이상까지 잘 복원**해버림 ("over-generalization") → anomaly signal 소멸
- 목표: **순수 Transformer(Attention + MLP)만으로**, 복잡한 모듈 없이, multi-class 통합 모델이 class-separated SOTA를 달성

## 핵심 아이디어 3가지 (The "Less Is More" Philosophy)

### 1. Noisy Bottleneck — Dropout이면 충분하다
- Encoder와 Decoder 사이에 **단일 MLP 병목** 배치
- 별도 노이즈 모듈 없이, MLP에 내장된 **Dropout(p=0.2)**만 활성화하여 정상 feature에 무작위 마스킹 적용
- Dropout이 denoising autoencoder 효과를 내어 정상은 복원 가능하지만, 이상은 복원 불가하게 함 (identity mapping 차단)

### 2. Linear Attention — 집중하지 못하는 것이 장점
- Decoder의 Self-Attention을 **Softmax Attention 대신 Linear Attention**으로 교체
- Softmax Attention은 특정 위치에 집중하여 정보를 그대로 전달(identity mapping)하는 경향이 있음
- Linear Attention은 집중을 분산시켜 전체 이미지 정보를 활용해 복원하도록 강제하여 동일 정보 전달 차단

### 3. Loose Reconstruction — 느슨하게 복원할수록 강하다
- **Loose Constraint (LC):** Encoder의 여러 layer feature를 그룹으로 묶어 합산 후 복원하여 Decoder에 자유도를 부여
- **Loose Loss (LL):** 이미 잘 복원된 정상 영역의 gradient를 축소(hard mining)하여 복원이 어려운 영역에 집중

## 학습 / 추론 흐름

학습:
```
image → ViT Encoder (frozen) → MLP Bottleneck (Dropout 0.2) → ViT Decoder (Linear Attention) → Loss
```

추론 (Dropout 비활성화):
```
image → ViT Encoder → MLP Bottleneck → ViT Decoder → Anomaly Map (Cosine Distance)
```

- **Encoder(Teacher)는 고정**, **Bottleneck + Decoder만 학습**
- Anomaly map = 2개 그룹의 per-pixel cosine distance 평균

## 주요 결과 (논문 발췌)

- MVTec AD (ViT-Base, Multi-class 통합): **I-AUROC 99.6% / P-AUROC 98.4% / AUPRO 94.8%**
- VisA: I-AUROC **98.7%** / Real-IAD: I-AUROC **89.3%**
- 스케일링 효과: ViT-Small(99.2%) → ViT-Base(99.6%) → ViT-Large(99.7%)로 성능 지속 향상

## PatchCore·SimpleNet·RD와의 차별점

| 항목 | PatchCore (method1) | SimpleNet (method2) | RD (method3) | Dinomaly (method4) |
|---|---|---|---|---|
| 핵심 메커니즘 | Memory bank + NN | Discriminator | 복원 오차 | **ViT 복원 + Loose 제약** |
| 백본 | WideResNet-50 | WideResNet-50 | WideResNet-50 | **ViT-Base/14 (DINOv2)** |
| Identity mapping 대응 | n/a | Gaussian noise | OCBE 병목 | **Dropout + Linear Attention** |
| Multi-class 지원 | class-separated | class-separated | class-separated | **Multi-class 통합 모델** |

## 본 재현 진행 상황

### 환경 구축 및 sanity check (진행 중)
- upstream: [guojiajeremy/Dinomaly](https://github.com/guojiajeremy/Dinomaly) 공식 구현체
- 김준아 학생 Dinomaly 구현체 기반 환경 셋업 완료
- `bottle` 카테고리 cross-check 수행 중

### 다음 단계
1. `bottle` sanity check 수치 검증 완료
2. MVTec AD 15개 전 카테고리 확장 재현 실행
3. 4-way 통합 비교 대시보드 업데이트

> 실행 가이드: [`../source/README.md`](../source/README.md)
