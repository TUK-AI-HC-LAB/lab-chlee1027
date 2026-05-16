# PatchCore 환경 재현성 확보 결과 (Environment Reproducibility)

## 1. 개요
PyTorch/CUDA 버전 및 라이브러리 의존성에 따른 성능 편차를 최소화하고 다른 환경에서도 동일한 결과를 얻기 위해, 실제 실험이 수행된 코랩 환경의 전체 의존성을 스냅샷 형태로 기록하여 재현성을 확보합니다.

## 2. 의존성 명시화 및 스냅샷 (완료)
*   **Requirements 스냅샷:** 현재 실험이 성공적으로 수행된 Colab(T4) 환경의 모든 라이브러리 버전을 `pip freeze`를 통해 추출하여 저장하였습니다.
    *   대상 파일: `method1_patchcore/source/requirements.txt`
*   **런타임 정보 기록:** Python 3.12, PyTorch 2.10.0+cu128, CUDA 12.8 정보와 GPU 모델명(T4)을 README와 요구사항 파일에 명시하였습니다.

## 3. 실행 환경 및 시드 고정
*   **결정론적 연산 (Deterministic Ops):** `torch.use_deterministic_algorithms(True)` 및 `CUBLAS_WORKSPACE_CONFIG` 설정을 통해 GPU 연산의 무작위성을 억제합니다.
*   **로그 기록 강화:** 실행 시 사용된 모든 하이퍼파라미터와 환경 정보를 결과 CSV와 함께 저장하여, 추후 동일 환경 구축 시 즉시 대조 가능하도록 구성하였습니다.

## 4. 기대 효과
*   `requirements.txt`를 통한 동일 패키지 설치만으로 추가적인 도구 없이 즉각적인 환경 복구가 가능합니다.
*   `pill` 카테고리와 같이 미세한 수치 차이가 발생하는 항목에 대해 환경 탓이 아닌 알고리즘적 원인 분석에 집중할 수 있는 베이스라인을 제공합니다.
