# SimpleNet: A Simple Network for Image Anomaly Detection and Localization

## 1. 개요 (Overview)
- **논문명:** SimpleNet: A Simple Network for Image Anomaly Detection and Localization
- **목적:** 산업용 이미지의 이상 탐지(Anomaly Detection) 및 위치 추정(Localization)을 위한 간단하고 효율적인 네트워크 제안.
- **주요 성과:**
  - MVTec AD 데이터셋 기준 99.6% AUROC 달성 (기존 SOTA 대비 오류 55.5% 감소).
  - RTX 3080 Ti 기준 77 FPS의 빠른 추론 속도 확보.

## 2. 기존 연구의 한계 (Limitations of Previous Works)
- **Reconstruction-based:** 정상 이미지만으로 학습하여 비정상 이미지를 복원하지 못할 것이라 가정하지만, 종종 비정상 영역도 잘 복원해버리는 문제 발생.
- **Synthesizing-based:** 정상 이미지에 가짜 이상(anomaly)을 합성하여 학습하지만, 합성된 이상이 실제 불량의 형태와 잘 맞지 않는 경우가 많음.
- **Embedding-based (e.g., PatchCore):** ImageNet에서 사전 학습된 특징을 그대로 사용할 경우 산업용 이미지와의 분포 차이(Domain Bias)로 인해 성능이 제한되거나 계산량/메모리 요구량이 높음.

## 3. SimpleNet의 핵심 구조 (Architecture)
SimpleNet은 4가지 주요 컴포넌트로 구성됩니다. 추론(Inference) 시에는 Anomaly Feature Generator가 제거되어 단일 스트림으로 빠르게 동작합니다.

1. **Feature Extractor (특징 추출기):**
   - 사전 학습된 백본(주로 WideResNet50)을 사용하여 로컬 특징을 추출.
2. **Feature Adaptor (특징 어댑터):**
   - 단일 Fully-Connected(FC) layer를 사용하여 사전 학습된 특징을 타겟 도메인(산업용 이미지)에 맞게 투영(Projection). 도메인 편향을 줄여줌.
3. **Anomaly Feature Generator (이상 특징 생성기 - 학습 시에만 사용):**
   - 특징 공간(Feature space)에서 어댑터를 통과한 정상 특징에 가우시안 노이즈($\mathcal{N}(\mu, \sigma^2)$)를 더해 가상의 '이상 특징'을 생성. 이미지 공간에 직접 노이즈를 합성하는 것보다 훨씬 효과적.
4. **Discriminator (판별기):**
   - 2-layer MLP 구조. 정상 특징(양성)과 생성된 이상 특징(음성)을 구별하도록 학습됨.

## 4. 학습 및 추론 (Training & Inference)
- **Loss Function:** Truncated L1 loss를 사용하여 판별기를 학습.
- **Inference:** 테스트 이미지가 들어오면 `Extractor` $\rightarrow$ `Adaptor` $\rightarrow$ `Discriminator`를 순차적으로 통과. Discriminator의 출력이 이상 점수(Anomaly Score)가 되며, 점수가 가장 높은 영역이 불량 위치로 추정.

## 5. 결론 및 의의 (Conclusion)
- 매우 단순한 신경망 모듈(FC layer, MLP, Gaussian Noise)만으로 구성되어 있어 학습과 적용이 쉬움.
- 기존의 복잡한 통계적 모델링이나 메모리 뱅크(Memory Bank) 방식 없이도 높은 정확도와 빠른 속도를 동시에 달성하여, 학술적 연구와 산업 현장 적용 사이의 간극을 줄임.
