# 논문 요약: Anomaly Detection via Reverse Distillation (CVPR 2022)

## 1. 개요 (Abstract)
- **Knowledge Distillation (KD)** 기법을 이상 탐지에 적용.
- 기존 KD AD의 한계(Teacher와 Student가 동일한 구조를 가짐)를 극복하기 위해 **Reverse Distillation (RD)** 패러다임 제안.
- Teacher Encoder와 Student Decoder로 구성된 T-S 모델 사용.

## 2. 핵심 아이디어
### 2.1 Reverse Distillation (역증류)
- **Conventional KD**: Teacher(Encoder) -> Student(Encoder)
- **Reverse Distillation**: Teacher(Encoder) -> OCBE(Bottleneck) -> Student(Decoder)
- Student Decoder가 Teacher Encoder의 특징을 '복원'하는 방식으로 학습하여, 정상 데이터의 패턴은 잘 복원하고 이상치는 복원하지 못하게 함.

### 2.2 One-Class Bottleneck Embedding (OCBE)
- **MFF (Multi-scale Feature Fusion)**: Teacher의 다양한 레이어(low to high level) 특징을 결합.
- **OCE (One-Class Embedding)**: 특징을 압축하여 정상 패턴의 정수만 남기고 이상치 노이즈를 차단하는 병목 역할.

## 3. 성능 (MVTec AD)
- **I-AUROC**: 평균 98.5%
- **P-AUROC**: 평균 97.8%
- **PRO**: 평균 93.9%
- **특징**: 추론 속도가 매우 빠르고(0.31s/img), 메모리 사용량이 적음 (352MB).

## 4. SimpleNet/PatchCore와의 차이점
- **PatchCore**: Memory bank 기반, 이웃 특징 검색 방식.
- **SimpleNet**: Discriminator(GAN-like) 기반, 가상 이상치 생성 방식.
- **Reverse Distillation**: Encoder-Decoder 구조 기반, 특징 복원 오차 방식.
