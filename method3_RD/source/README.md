# method3_RD — 실행 가이드

Reverse Distillation (Deng et al. 2022, *Anomaly Detection via Reverse Distillation from One-Class Embedding*, CVPR 2022) 재현·실험을 위한 source 디렉토리입니다.

> 현재 단계: **실험 진행 중** — `toothbrush` 카테고리 재현 완료 (1/15).

## 환경 (확정)

- Colab T4 GPU, Python 3.12
- PyTorch 2.10.0+cu128 (Colab 기본)
- WideResNet-50 (Teacher Encoder, ImageNet pretrain)
- upstream: [hq-deng/RD4AD](https://github.com/hq-deng/RD4AD) (공식 구현체)

## 데이터 준비

method1·2와 동일한 MVTec AD 구조 재사용. `hq-deng/RD4AD`는 코드 루트의 `mvtec/` 폴더를 참조하므로 심볼릭 링크 또는 복사로 대응함.

```
<RD_DIR>/mvtec/
├── bottle/
├── toothbrush/
└── ...
```

- 로컬 데이터 위치: `C:\Users\채현\OneDrive\바탕 화면\TUK\mvtec_anomaly_detection`

## 실행

```bash
# toothbrush 카테고리 재현 실행
CATEGORY=toothbrush MVTEC_DIR="C:\Users\채현\OneDrive\바탕 화면\TUK\mvtec_anomaly_detection" bash run_baseline.sh
```

> `main.py`가 전체 카테고리를 순회하는 방식일 경우, `toothbrush`만 실행하도록 코드를 일부 수정하여 효율화할 수 있음.

method1·2와 동일하게 sh 스크립트 또는 노트북 + 결과 csv + commit hash 3줄로 재현 출처를 남길 예정.

## 핵심 구조 (논문 요약 참조)

- **Teacher Encoder**: pretrained 백본(WRN-50 등)에서 multi-level feature 추출
- **OCBE (One-Class Bottleneck Embedding)**: 정상 패턴의 정수만 남기는 병목
  - **MFF (Multi-scale Feature Fusion)**: Teacher의 low~high level feature 결합
  - **OCE (One-Class Embedding)**: feature 압축, 이상치 노이즈 차단
- **Student Decoder**: Teacher Encoder의 feature를 복원하도록 학습 — 정상은 복원 잘 됨, 이상은 복원 실패
- **이상 점수**: Teacher feature vs Student 복원 feature 간 cosine similarity 차이

자세한 내용: [../markdown/rd_summary.md](../markdown/rd_summary.md)

## PatchCore·SimpleNet과의 차별점 (요약)

| 항목 | PatchCore | SimpleNet | Reverse Distillation |
|---|---|---|---|
| 핵심 메커니즘 | Memory bank + NN | Discriminator (GAN-like) | Encoder-Decoder 복원 오차 |
| 학습 필요? | ❌ | ✅ (Adaptor + Discriminator) | ✅ (Student Decoder) |
| 이상 신호 | NN 거리 | Discriminator 점수 | feature 복원 오차 |
| 추론 메모리 | memory bank | MLP 가중치 | Decoder 가중치 (~352MB) |
| 추론 속도 (논문) | NN 검색 비용 | ~77 FPS | ~0.31s/img |
| MVTec AD 평균 I-AUROC (논문) | 99.1~99.6% | 99.6% | 98.5% |

## 결과 (실시간 업데이트)

| Category | I-AUROC | Full P-AUROC | Anomaly P-AUROC | Status |
|---|---|---|---|---|
| bottle | - | - | - | Planning |
| toothbrush | 0.994 | 0.991 | 0.945 | Done |
| ... | - | - | - | - |

> 우선순위 카테고리: method1·2에서 동일하게 다룬 카테고리(bottle, toothbrush)부터 시작해 3-way 직접 비교.

## 재현 출처 (가이드 형식 — commit/sh/csv 3줄)

- commit: `[커밋해시]`
- sh: `method3_RD/source/run_baseline.sh`
- csv: `method3_RD/source/results/` (1/15 완료)

## 다음 단계

1. upstream 구현 후보 확정 (`hqucl/Reverse-Distillation` 코드 분석 후 결정)
2. method1·2와 동일한 환경(Colab T4, MVTec AD)에서 baseline 실행 — bottle, toothbrush 우선
3. PatchCore·SimpleNet 결과와 3-way 비교 (`../markdown/baseline_full_table.md` 신설 예정)
4. 비교 분석 노트 작성 — `../markdown/rd_vs_patchcore_simplenet.md` (예정)
