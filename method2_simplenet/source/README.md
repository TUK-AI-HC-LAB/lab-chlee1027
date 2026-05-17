# method2_simplenet — 실행 가이드

SimpleNet (Liu et al. 2023, *SimpleNet: A Simple Network for Image Anomaly Detection and Localization*, CVPR 2023) 재현·실험을 위한 source 디렉토리입니다.

> 현재 단계: **1·2차 재현 완료 (toothbrush, bottle — 2/15)** — 논문 요약 ([../markdown/simplenet_summary.md](../markdown/simplenet_summary.md)), 실험 노트북 (`simplenet_colab.ipynb`), 결과 csv (`results/baseline_toothbrush.csv`, `results/baseline_bottle.csv`), 통합 테이블 ([../markdown/baseline_full_table.md](../markdown/baseline_full_table.md)).

## 환경

- Colab T4 GPU, Python 3.12
- PyTorch 2.10.0+cu128 (Colab 기본)
- pandas 최신 (≥2.0, upstream의 `df.append()` 호출은 deprecated → 아래 수정 내역 참고)
- upstream: [DonaldRR/SimpleNet](https://github.com/DonaldRR/SimpleNet) — `main` 브랜치

## 데이터 준비

method1과 동일한 MVTec AD 구조 재사용.

```
<MVTEC_DIR>/
├── bottle/
│   ├── train/good/...
│   └── test/{good,...}/...
└── ...
```

- Colab: Google Drive 마운트 후 `/content/drive/MyDrive/anormaly_detection/mvtec` 사용
- 로컬: lab repo 루트의 `mvtec_anomaly_detection/` 그대로 활용 가능

## 실행 (1차 — 노트북)

1차 재현은 `simplenet_colab.ipynb` 한 파일에서 실행. 셀 순서:

1. upstream zip 다운로드·압축해제
2. Google Drive 마운트
3. `metrics.py` 수정 (아래 "수정 내역" 참고)
4. `python main.py ...` 로 학습+평가
5. 결과 csv 확인

### 1차 실행 명령 (toothbrush, `simplenet_colab.ipynb` 셀 3)

```bash
python3 main.py \
  --gpu 0 --seed 0 \
  --log_group simplenet_mvtec \
  --log_project MVTecAD_Results \
  --results_path results \
  --run_name toothbrush_visual \
  --save_segmentation_images \
  net \
    -b wideresnet50 \
    -le layer2 -le layer3 \
    --pretrain_embed_dimension 1536 \
    --target_embed_dimension 1536 \
    --patchsize 3 \
    --meta_epochs 40 \
    --embedding_size 256 \
    --gan_epochs 4 \
    --noise_std 0.015 \
    --dsc_hidden 1024 \
    --dsc_layers 2 \
    --dsc_margin .5 \
    --pre_proj 1 \
  dataset \
    --batch_size 8 \
    --resize 256 --imagesize 224 \
    -d toothbrush \
    mvtec /content/drive/MyDrive/anormaly_detection/mvtec
```

## 수정 내역 (upstream 대비)

1. **`metrics.py`**: pandas 2.0+ 호환성을 위해 `df.append()`를 `df.loc[len(df)] = ...`로 수정.
2. **`main.py`**: 시각화 버그 수정을 위해 주석 처리된 `test()` 호출을 활성화하고, `train()` 완료 후 자동으로 시각화가 실행되도록 로직 추가.
3. **`simplenet_colab.ipynb`**: 위 패치들을 자동 실행 셀로 포함하고, 결과 이미지를 수직으로 나열하여 출력하는 셀 추가.

## 핵심 구조 (논문 요약 참조)

- **Feature Extractor**: pretrained 백본(WRN-50)에서 mid-level patch feature 추출
- **Feature Adaptor**: 단일 FC layer로 ImageNet feature를 산업 도메인으로 투영 (domain bias 완화)
- **Anomaly Feature Generator**: 학습 시에만 사용 — 정상 feature에 Gaussian noise 더해 가상 이상 feature 생성
- **Discriminator**: 2-layer MLP로 정상/생성된 이상 feature 분류

추론 시 generator는 빠지고 Extractor → Adaptor → Discriminator 단일 stream으로 동작.

자세한 내용: [../markdown/simplenet_summary.md](../markdown/simplenet_summary.md)

## 결과

### 1차 재현 (toothbrush, 2026-05-17)

| 지표 | 재현 | 비고 |
|---|---|---|
| Instance AUROC | **1.000** | 논문 수치와 동등 |
| Full Pixel AUROC | **0.985** | 이전(0.983) 대비 소폭 상승 |
| Anomaly Pixel AUROC | **0.915** | 이전(0.904) 대비 상승, 시각화 확인 완료 |

- 결과 csv: `results/baseline_toothbrush.csv` (5/16, 5/17 통합 기록)
- 노트북: `simplenet_colab.ipynb` (실행 결과 포함)
- **시각화**: 히트맵 생성 성공 및 노트북 내 수직 나열 출력 확인.

## 재현 출처 (가이드 형식 — commit/sh/csv 3줄)

### 1차 — toothbrush (2026-05-17)

- commit: (push 시점 채움)
- sh / 노트북: `method2_simplenet/source/simplenet_colab.ipynb`
- csv: `method2_simplenet/source/results/baseline_toothbrush.csv`

## 다음 단계

- 다른 카테고리(bottle, leather, pill, metal_nut 등)로 확장 — method1과 동일 카테고리에서 직접 비교
- 노트북 → 셸 스크립트화: `run_baseline.sh` (CATEGORY 환경변수)
- 카테고리별 csv 누적 후 method1 PatchCore 결과(`../method1_patchcore/markdown/baseline_full_table.md`)와 비교표 작성
- 비교 분석: `../markdown/simplenet_vs_patchcore.md` (예정)
