# Dinomaly — 논문 요약

> 원문 PDF: `method4_Dinomaly/paper/` (배치 예정)

## 한 줄 요약

(논문 분석 후 작성 예정)

## 문제 / 동기

- **Cold-start anomaly detection** 동일 — 정상만 있고 비정상은 거의 없는 산업 환경
- (기존 접근의 한계 — 논문 분석 후 작성 예정)

## 핵심 아이디어

(논문 분석 후 작성 예정)

## 주요 결과 (논문 발췌)

(논문 분석 후 작성 예정)

## PatchCore·SimpleNet·RD와의 차별점

| 항목 | PatchCore (method1) | SimpleNet (method2) | RD (method3) | Dinomaly (method4) |
|---|---|---|---|---|
| 핵심 메커니즘 | Memory bank + NN | Discriminator (GAN-like) | Encoder-Decoder 복원 오차 | (작성 예정) |
| 학습 필요? | ❌ | ✅ | ✅ | (작성 예정) |
| MVTec AD 평균 I-AUROC | 99.1~99.6% | 99.6% | 98.5% | (작성 예정) |

## 본 재현 진행 상황

### 환경 구축 및 sanity check (진행 중)
- 김준아 학생 Dinomaly 구현체 fork 기반 환경 셋업
- `bottle` 카테고리 cross-check 진행 중

### 다음 단계

1. 환경 구축 및 bottle sanity check 완료
2. 15개 전 카테고리 확장 재현
3. 4-way 비교 분석 노트 작성
