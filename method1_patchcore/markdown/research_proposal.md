# [Refined] PatchCore 한계 극복 및 Method 1~4 통합 연구 제안서 (v2)

본 문서는 PatchCore, SimpleNet, RD, Dinomaly의 재현 및 비교 분석 결과를 토대로, 각 알고리즘의 핵심 메커니즘을 융합하여 기존 PatchCore의 한계를 보완하는 후속 연구 방향을 제안함.

---

## 1. [주제 A] 관계 추론 및 Attention 기반 논리적 이상 탐지 (Contextual Logical AD)

### 1.1 개요 및 동기
- **PatchCore (M1)의 약점**: 로컬 패치 특징에 의존하는 구조적 특성상, 부품의 구성 요소는 정상이지만 배치 관계나 개수가 어긋난 '논리적 결함(Logical Anomaly)' 탐지에 한계가 있음.
- **Dinomaly (M4)의 강점**: **Linear Attention**을 통해 이미지 전반의 전역적 문맥 정보를 파악하는 데 유리함.
- **통합 아이디어**: PatchCore의 메모리 뱅크 체계에 Dinomaly의 **Attention-based contextual encoding을 결합**. 패치 특징과 함께 Attention Map 기반의 **"Relational Context"**를 결합 저장하여, 공간적 위상 관계 이상을 포착함.

### 1.2 관련 연구 대비 차별성
| 기존 연구 | 주요 특징 | 본 제안 방식의 차별점 (Contribution) |
| :--- | :--- | :--- |
| **PNI** (ICCV '23) | 패치의 절대 좌표 정보를 MLP로 학습 | 절대 좌표 의존성 탈피 및 **M4의 Attention 기반 관계 특징** 활용 |
| **GraphCore** (ICLR '23) | Rotation-invariant feature representation 중심 | **Logical anomaly** 탐지를 위한 relational context reasoning에 집중 |

### 1.3 기대 효과 및 한계
- **장점**: MVTec LOCO AD 등 최신 벤치마크 대응에 유리하며, 설명 가능한(Explainable) AD로의 확장성이 높음.
- **단점**: 패치 간 관계 데이터(Edge) 추가에 따른 메모리 사용량 및 연산량 최적화가 필요함.

---

## 2. [주제 B] MUAD 기반 고효율 지속 가능 메모리 큐레이션 (Unified Continual Memory)

### 2.1 개요 및 동기
- **PatchCore (M1)의 약점**: 새로운 정상 패턴이 유입될수록 **메모리 사용량이 지속 증가**하여 장기적인 배포 환경에서 관리 부담이 발생함.
- **Dinomaly (M4)의 강점**: **MUAD (Multi-class Unified)** 철학을 통해 여러 클래스를 단일 모델로 효율적으로 관리함.
- **통합 아이디어**: 클래스별로 분절된 메모리를 **"통합 메모리 뱅크(Unified Bank)"**로 재구성하고, **RD (M3)의 복원 오차(Reconstruction Error)**를 정보량 지표로 활용함. 정보 엔트로피(상세 metric은 후속 정의 예정) 및 참조 빈도(Usage frequency)에 기반한 동적 삭제(Eviction) 전략을 통해 메모리 사이즈를 **bounded memory budget** 내에서 관리함.

### 2.2 관련 연구 대비 차별성
| 구분 | 기존 연구 (Memory compression variants) | 본 제안 방식 (Unified Curation) |
| :--- | :--- | :--- |
| **접근** | 수학적 압축 (PQ, 차원 축소) 등 정적 최적화 중심 | **M4의 통합 학습 및 M3의 정보 변별력**을 활용한 동적 관리 |
| **장점** | 저장 용량 감소 | Continual AD 환경에서 성능 하락을 최소화하며 신규 정보 수용력 확보 |

---

## 3. [주제 C] 도메인 적응형 동적 패치 시스템 (Domain-adaptive Patching)

### 3.1 개요 및 동기
- **PatchCore (M1)의 약점**: ImageNet 사전학습 모델의 표현력에 의존하여 산업 데이터와의 도메인 갭 발생 및 영역별 연산 낭비 발생.
- **SimpleNet (M2)의 강점**: **Feature Adapter**를 통한 산업 도메인 특징 공간으로의 효과적 정렬 능력.
- **통합 아이디어**: PatchCore 전단에 SimpleNet 스타일의 **Lightweight Adapter**를 결합하여 도메인 적응을 수행함과 동시에, 영역별 정보 엔트로피에 따라 패치 해상도를 동적으로 조절함(복잡 영역: 정밀, 단순 영역: 성기게 처리).

### 3.2 관련 연구 대비 차별성
- 모든 위치에 다중 스케일을 고정 적용하는 기존 방식(CFA 등)과 달리, **도메인 특화 어댑터**가 영역의 중요도를 판단하여 선택적 스케일을 적용함으로써 실무적인 연산 효율성을 극대화함.

---

## 4. 실험 계획 (Experimental Plan)

### 4.1 대상 데이터셋
- **MVTec LOCO AD**: 주제 A(Logical AD) 검증을 위한 필수 데이터셋.
- **MVTec AD & VisA**: 주제 B, C의 범용성 및 Continual Learning 시나리오 검증.

### 4.2 비교 대상 (Baselines)
- **PatchCore (Original)**: 기본 성능 및 메모리 점유율 베이스라인.
- **EfficientAD, SimpleNet**: 연산 효율 및 도메인 적응 성능 비교군.

### 4.3 평가지표 (Metrics)
- **I-AUROC / P-AUROC**: 탐지 및 위치추정 기본 성능.
- **Memory Footprint / Inference Time**: 주제 B, C의 실용적 가치 증명.
- **sAUROC (Structural) / lAUROC (Logical)**: MVTec LOCO 기반의 결함 종류별 탐지 능력.

---

## 5. 결론 및 건의

본 제안은 직접 재현한 4개 알고리즘의 공학적 분석을 기반으로 함. 특히 **주제 A(Logical AD)**를 메인 연구 방향으로 설정하되, **주제 B와 C**를 최적화 모듈로 활용한다면 학술적 참신성과 산업적 실용성을 모두 확보한 수준 높은 논문 작성이 가능할 것으로 판단됨. 교수님의 검토 및 방향 지도를 요청함.

---

## References
- PatchCore (CVPR 2022)
- PNI (ICCV 2023)
- EfficientAD (WACV 2024)
- CFA (CVPR 2022)
- GraphCore (ICLR 2023)
- SimpleNet (CVPR 2023)
- Dinomaly (CVPR 2025)
