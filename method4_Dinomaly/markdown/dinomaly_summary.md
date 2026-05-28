# Guo et al. 2025 — Dinomaly: The Less Is More Philosophy in Multi-Class Unsupervised Anomaly Detection

## Paper Metadata

| 항목 | 내용 |
|---|---|
| 제목 | Dinomaly: The Less Is More Philosophy in Multi-Class Unsupervised Anomaly Detection |
| 저자 | Jia Guo, Shuai Lu, Weihang Zhang, Fang Chen, Huiqi Li, Hongen Liao |
| 학회/저널 | CVPR |
| 연도 | 2025 |
| 논문 링크 | [CVPR 2025 Open Access](https://openaccess.thecvf.com/content/CVPR2025/html/Guo_Dinomaly_The_Less_is_More_Philosophy_in_Multi-Class_Unsupervised_CVPR_2025_paper.html) |
| GitHub / 공식 코드 | [guojiajeremy/Dinomaly](https://github.com/guojiajeremy/Dinomaly) |
| 조사 이유 | 단일 통합 가중치 모델로 다중 클래스 이상 탐지 성능을 획득하는 Multi-class Unified AD 모델 분석 및 재현을 위함 |

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

## 본 재현 진행 상황 (2026-05-25 완료)

- **재현 완결**: MVTec AD 15개 전 카테고리 재현 완료 (**Mean I-AUROC 0.9962**)
- **수치 일치**: 김준아 학생 베이스라인 수치와 소수점 4자리까지 완벽 일치 확인.
- **분석 보고**: 4-way 통합 비교 프레임워크 반영 및 카테고리별 편차 분석 완료.

## 📈 카테고리별 재현 편차 분석 (Category Deviation Analysis)

이번 재현 실험에서 나타난 카테고리별 성능 차이를 Dinomaly의 구조적 특성과 연계하여 분석함.

### 1. 고성능 카테고리 (I-AUROC 1.000): `bottle`, `leather`, `tile` 등
*   **특징**: 피사체의 배경이 단순하거나(bottle), 질감이 일정한(leather, tile) 경우.
*   **분석**: Dinomaly의 **Linear Attention**이 배경의 불필요한 노이즈를 효과적으로 배제하고, 정상 질감의 특징을 **Loose Reconstruction**을 통해 안정적으로 복원해내기 때문에 이상치와의 대조가 명확히 발생함.

### 2. 상대적 저조 카테고리 (I-AUROC 0.980 내외): `capsule` (0.979), `screw` (0.985)
*   **특징**: 결함 부위가 매우 미세하거나(screw의 작은 흠집), 객체의 형태가 복잡한 경우.
*   **분석**: Dinomaly의 **Loose Reconstruction** 방식은 특징점들을 그룹화하여 '느슨하게' 복원하기 때문에, 픽셀 단위의 극도로 미세한 변화는 '정상적인 복원 오차' 범위 내에 포함될 가능성이 있음. 이는 PatchCore와 같은 Memory-bank 방식이 미세 결함에 더 민감하게 반응하는 것과 대조적인 특징임.

### 3. 종합 결론
Dinomaly는 단일 통합 모델(Multi-class)임에도 불구하고 대부분의 카테고리에서 개별 모델(Class-separated)보다 우수한 성능을 보임. 다만, **미세 구조 결함**이 중요한 카테고리에서는 **Noisy Bottleneck**의 강도를 조절하거나 해상도를 높이는 등의 추가 튜닝이 성능 향상의 열쇠가 될 것으로 판단됨.

### 4. MUAD(Multi-class Unified)의 실용적 우위
- **기존 방식 (M1~M3)**: 카테고리별로 독립된 모델 학습 및 저장이 필요함 (MVTec AD 기준 15개의 모델 파일 발생).
- **Dinomaly 방식 (M4)**: 단 **하나의 모델(Single Weight)**로 15개 전체 카테고리의 정상 패턴을 동시에 학습하고 추론함. 
- **의의**: 모델 관리 비용과 메모리 점유율을 1/15로 획득하면서도, 개별 학습 모델보다 높은 평균 성능(0.9962)을 달성하여 실제 산업 현장에서의 배포 효율성이 비약적으로 높음.

> 실행 가이드: [`../source/README.md`](../source/README.md)
