# PatchCore 환경 재현성 확보 계획 (Environment Reproducibility Plan)

## 1. 개요
W20 피드백에 따라, PyTorch/CUDA 버전 및 라이브러리 의존성에 따른 성능 편차를 최소화하고 다른 환경에서도 동일한 결과를 얻기 위한 단계별 재현성 확보 계획을 수립합니다.

## 2. 단기 계획: 의존성 명시화
*   **Requirements 추출:** 현재 실험이 성공적으로 수행된 Colab/로컬 환경의 라이브러리 버전을 `freeze`하여 저장합니다.
    *   대상 파일: `method1_patchcore/source/requirements.txt`
*   **런타임 정보 기록:** Python 버전, PyTorch 버전, CUDA 버전, GPU 모델명을 README 상단에 명시합니다.

## 3. 중기 계획: 실행 스냅샷 및 시드 고정
*   **결정론적 연산 (Deterministic Ops):** `torch.use_deterministic_algorithms(True)` 및 `CUBLAS_WORKSPACE_CONFIG` 설정을 스크립트에 추가하여 GPU 연산의 무작위성을 억제합니다.
*   **로그 기록 강화:** 실행 시 사용된 모든 하이퍼파라미터와 환경 정보를 결과 CSV와 함께 저장하도록 스크립트를 보완합니다.

## 4. 장기 계획: Docker 기반 컨테이너화
*   **Dockerfile 작성:** `nvidia/cuda` 베이스 이미지를 활용하여 OS 수준부터 동일한 환경을 구축합니다.
*   **환경 일치화:** 데이터셋 경로와 출력 경로를 볼륨 마운트로 고정하여 어느 머신에서나 `docker run` 만으로 재현 가능하게 구성합니다.

## 5. 기대 효과
*   `pill` 카테고리와 같이 미세한 수치 차이가 발생하는 항목에 대해 환경 탓이 아닌 알고리즘적 원인 분석에 집중할 수 있음.
*   추후 SimpleNet 등 타 알고리즘과의 비교 실험 시 동일한 베이스라인(CUDA/Python) 유지가 용이함.
