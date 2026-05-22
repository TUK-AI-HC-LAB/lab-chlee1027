# Reverse Distillation Baseline 재현 분석 (MVTec AD 14/15 진행)

> 재현 실행: 2026-05-21, Colab T4 GPU
> 논문: Deng et al. 2022 — `method3_RD/paper/Reverse_Distillation_CVPR2022.pdf`
> 논문 요약: `method3_RD/markdown/rd_summary.md`
> 상세 결과: `method3_RD/markdown/baseline_full_table.md`
> 3-way 비교: `method3_RD/markdown/rd_vs_patchcore_simplenet.md`

## 1. 개요 및 목적
Reverse Distillation(RD) baseline을 MVTec AD에서 재현하여, PatchCore(method1)·SimpleNet(method2)와 동일 조건에서 비교 가능한 세 번째 기준선을 확보한다. 현재 14/15 카테고리 완료(잔여: hazelnut).

## 2. 실험 환경 및 설정
- **환경**: Colab T4 GPU
- **기술 스택**: Python 3.12, torch 2.x
- **upstream**: [hq-deng/RD4AD](https://github.com/hq-deng/RD4AD) (공식 구현체)
- **Backbone**: WideResNet-50 (Teacher Encoder, ImageNet pretrain) + de-WideResNet-50 (Student Decoder)
- **학습 설정**: img 256, batch 16, lr 0.005, epochs 200
- **수정**: `test.py` pandas 호환(`df.append`→`pd.concat`), `main_single.py` 단일 카테고리 실행 래퍼 (상세: `../source/README.md`)

## 3. 종합 결과 (14/15 카테고리)
- **I-AUROC 평균**: 0.987
- **Full P-AUROC 평균**: 0.978

원논문 Table 1·2의 "Ours(WResNet50, 256)" 값(I 0.985 / P 0.977)과 대조한 결과 **ΔI +0.002, ΔP +0.001로 거의 완벽히 일치** — 재현 성공. grid·leather·metal_nut·wood에서 I-AUROC 1.000을 달성했다.

> **논문 대조 완료:** `baseline_full_table.md`의 paper 컬럼을 원논문 PDF Table 1·2에서 직접 전사하여 정정함. 대부분 카테고리가 Δ ±0.01 내로 정확히 재현됨.

## 4. 주요 관찰 및 인사이트
- **강점 (텍스처 픽셀 정밀도):** `wood` P-AUROC 0.987은 PatchCore(0.951)·SimpleNet(0.940)을 크게 상회. encoder-decoder 복원 방식이 텍스처 결함의 픽셀 경계를 잘 잡는다. `screw`(0.996)·`leather`(0.994)·`grid`(0.993)도 픽셀 최고 수준.
- **약점 (다양 패턴 카테고리):** `cable`(I 0.959)·`transistor`(I 0.970/P 0.928)에서 세 method 중 최저. 부품 위치·배선처럼 정상 패턴 변이가 큰 카테고리에서 복원 모델이 불리.
- **bottle 픽셀:** I-AUROC 0.996로 높지만 P-AUROC 0.955로 PatchCore(0.985)·SimpleNet(0.980) 대비 -0.03 낮음 — 이미지 탐지와 픽셀 정밀도가 갈리는 사례.
- **pill (PatchCore 약점 카테고리):** RD I-AUROC 0.965 / P-AUROC 0.982. PatchCore(I 0.967)와 비슷하지만 픽셀에서는 RD(0.982)가 PatchCore(0.978)보다 우위. 다만 이미지 탐지는 SimpleNet(0.986)이 최고.
- **method 간 상보성:** 이미지 탐지=SimpleNet, 범용 픽셀=PatchCore, 텍스처 픽셀=RD 구도가 드러남 (상세: `rd_vs_patchcore_simplenet.md`).

## 5. 결론
RD baseline을 14/15 카테고리에서 원논문과 거의 동일하게 재현(ΔI +0.002 / ΔP +0.001)했으며, 세 method의 3-way 비교 기반을 마련했다. 잔여 hazelnut 완료 후 15/15 평균을 확정하는 것이 다음 과제다.
