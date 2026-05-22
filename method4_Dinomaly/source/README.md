# method4_Dinomaly — 실행 가이드 및 재현 결과

Dinomaly (Guo et al. 2025, *Dinomaly: The Less Is More Philosophy in Multi-Class Unsupervised Anomaly Detection*, CVPR 2025) baseline을 MVTec AD에서 재현하기 위한 디렉토리입니다.

## 📊 재현 결과 요약

> ⏳ **진행 중** — 환경 구축 및 bottle 카테고리 sanity check 수행 중.

| Metric | Repro (Mean) | Paper (Mean) | Status |
| :--- | :---: | :---: | :---: |
| **I-AUROC** | — | 0.996 | 🔄 진행 중 |
| **P-AUROC** | — | 0.984 | 🔄 진행 중 |

*상세 수치는 재현 완료 후 [baseline_full_table.md](../markdown/baseline_full_table.md)에서 확인 가능합니다.*

---

## 🏛 Architecture & Mechanism

### [Method 4: Dinomaly] - Minimalist Reconstruction Based Anomaly Detection
> **핵심 특징:** DINOv2 사전학습 ViT Encoder의 중간층 feature를 Dropout 병목 + Linear Attention Decoder로 복원하며, 정상과 다른 '복원 실패' 오차를 감지하는 순수 Transformer 구조. Multi-class 통합 모델.

```mermaid
graph LR
    Input[Input Image] --> Encoder[ViT Encoder - DINOv2 Frozen]
    Encoder --> Bottleneck[MLP Bottleneck + Dropout]
    Bottleneck --> Decoder[ViT Decoder - Linear Attention]
    Decoder --> Recon[Reconstructed Features]
    
    Error{Cosine Distance}
    Encoder -- Original Feat --> Error
    Recon -- Restored Feat --> Error
    Error --> Score[Anomaly Map]
```

*   **Noisy Bottleneck:** MLP 내장 Dropout(p=0.2)으로 feature를 무작위 마스킹 → denoising 효과로 identity mapping 차단.
*   **Linear Attention:** Softmax 없이 attention을 분산시켜 동일 위치 정보 전달을 방지, 계산량도 절감.
*   **Loose Reconstruction:** 다층 feature를 그룹으로 묶어 느슨하게 복원 + hard mining loss로 이미 잘 복원된 영역의 gradient 축소.

---

## 🔍 집중 분석 및 결과 보고

1. **[dinomaly_summary.md](../markdown/dinomaly_summary.md):** 논문 요약 + 핵심 구조(Foundation ViT / Noisy Bottleneck / Linear Attention / Loose Reconstruction) + PatchCore·SimpleNet·RD와의 차별점

---

## 💻 환경 및 실행 가이드

### 환경 (Colab T4 기준)
- Python 3.12, CUDA 12.x
- PyTorch 2.x (Colab 기본)
- upstream: [guojiajeremy/Dinomaly](https://github.com/guojiajeremy/Dinomaly) (공식 구현체)

### 데이터 준비
method1~3과 동일한 MVTec AD 구조.
```
<MVTEC_DIR>/
├── bottle/
│   ├── train/good/...
│   └── test/{good,broken_large,...}/...
└── ...
```
- **Colab:** Google Drive 마운트 후 경로 지정.
- **로컬:** lab repo 루트의 `mvtec_anomaly_detection/` 활용 또는 `MVTEC_DIR` 환경변수로 지정.

### 실행 방법
```bash
# 특정 카테고리 실행 (예: bottle)
CATEGORY=bottle MVTEC_DIR=/path/to/mvtec bash run_baseline.sh
```
**스크립트 동작 과정:**
1. upstream [guojiajeremy/Dinomaly](https://github.com/guojiajeremy/Dinomaly)을 clone.
2. 필요 시 수정사항 적용.
3. 논문 기본 설정(ViT-Base/14, DINOv2-R, resize 448 / crop 392, 10,000 iterations)으로 학습+평가.

> 1차 탐색은 김준아 학생의 fork 기반 노트북으로 진행 예정.

## 🛠 수정 내역 (upstream 대비)

> 수정 내역은 실험 진행 후 기재 예정.

## 📂 폴더 구조 및 파일 가이드
- `source/README.md`: 실행 가이드 및 재현 결과 (본 문서).
- `source/run_baseline.sh`: 카테고리별 실험 자동화 쉘 스크립트 (작성 예정).
- `source/requirements.txt`: Colab T4 환경 패키지 스냅샷 (작성 예정).
- `source/results/`: 재현 결과 CSV.
- `markdown/`: 논문 요약, 재현 분석, 결과 테이블, 시각화.

## 📌 재현 출처 (가이드 형식 — commit/sh/csv 3줄)

### MVTec AD (진행 중)

- commit: (실험 완료 후 기재)
- sh / 노트북: `method4_Dinomaly/source/run_baseline.sh` / (노트북명)
- csv: `method4_Dinomaly/source/results/baseline_<category>.csv`
- 집계표: [`method4_Dinomaly/markdown/baseline_full_table.md`](../markdown/baseline_full_table.md)
