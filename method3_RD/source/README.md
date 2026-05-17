# method3_RD — 실행 가이드 (예정)

Reverse Distillation (Deng et al. 2022, *Anomaly Detection via Reverse Distillation from One-Class Embedding*, CVPR 2022) 재현을 위한 디렉토리입니다.

## 개요
- **상태**: 논문 요약 완료 및 구조 생성 (실험 계획 중)
- **핵심**: Encoder-Decoder 기반 지식 증류 모델
- **Upstream**: [hqucl/Reverse-Distillation](https://github.com/hqucl/Reverse-Distillation)

## 실행 계획
1. Upstream 코드 분석 및 환경 구축
2. MVTec AD 데이터셋 연동
3. `bottle`, `toothbrush` 등 핵심 카테고리 우선 재현
4. PatchCore, SimpleNet과의 성능 비교

## 결과 (예정)
| Category | I-AUROC | P-AUROC | PRO-AUROC | Status |
|---|---|---|---|---|
| bottle | - | - | - | Planning |
| toothbrush | - | - | - | Planning |
| ... | - | - | - | - |
