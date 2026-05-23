#!/usr/bin/env bash
# SimpleNet Ablation Study - 10개 실험 자동화 스크립트
#
# 실행 방법:
#   MVTEC_DIR=/path/to/mvtec bash run_ablation.sh

set -euo pipefail

MVTEC_DIR="${MVTEC_DIR:-$HOME/mvtec}"
SIMPLENET_DIR="${SIMPLENET_DIR:-$HOME/SimpleNet}"
WORK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 결과를 저장할 폴더 생성
mkdir -p "${WORK_DIR}/results/ablation"

# 공통 실행 함수
run_experiment() {
    local category=$1
    local seed=$2
    local noise=$3
    local epochs=$4
    local exp_name=$5

    echo "=========================================================="
    echo "🚀 [START] Experiment: $exp_name"
    echo "   Category: $category, Seed: $seed, Noise: $noise, Epochs: $epochs"
    echo "=========================================================="

    # main.py 실행 (run_baseline.sh의 로직 기반)
    cd "$SIMPLENET_DIR"
    python3 main.py \
        --gpu 0 \
        --seed "$seed" \
        --log_group ablation_study \
        --log_project MVTecAD_Results \
        --results_path results \
        --run_name "$exp_name" \
        net \
        -b wideresnet50 \
        -le layer2 \
        -le layer3 \
        --pretrain_embed_dimension 1536 \
        --target_embed_dimension 1536 \
        --patchsize 3 \
        --meta_epochs 40 \
        --embedding_size 256 \
        --gan_epochs "$epochs" \
        --noise_std "$noise" \
        --dsc_hidden 1024 \
        --dsc_layers 2 \
        --dsc_margin .5 \
        --pre_proj 1 \
        dataset \
        --batch_size 8 \
        --resize 329 \
        --imagesize 288 \
        -d "$category" \
        mvtec "$MVTEC_DIR"

    # 결과 CSV 복사 (경로는 upstream main.py의 로그 생성 규칙에 따라 다를 수 있음)
    # 일반적으로 results/MVTecAD_Results/ablation_study/<exp_name>/ 내에 생성됨
    # 가장 최근 생성된 csv 파일을 찾아 복사 시도
    local result_csv=$(find "results/MVTecAD_Results/ablation_study/$exp_name" -name "*.csv" | head -n 1)
    if [ -f "$result_csv" ]; then
        cp "$result_csv" "${WORK_DIR}/results/ablation/${exp_name}.csv"
        echo "✅ [DONE] Results saved to ablation/${exp_name}.csv"
    else
        echo "⚠️ [WARN] Result CSV not found for $exp_name"
    fi
}

# --- 🧪 10개 실험 리스트 ---

# 1-6) 확률적 변동성 확인 (Stochasticity) - 각 카테고리별 Seed 추가
# Baseline은 이미 seed 0으로 완료됨
run_experiment "screw"    100  0.015  4  "exp1_screw_seed100"
run_experiment "screw"    2026 0.015  4  "exp2_screw_seed2026"
run_experiment "capsule"  100  0.015  4  "exp3_capsule_seed100"
run_experiment "capsule"  2026 0.015  4  "exp4_capsule_seed2026"
run_experiment "bottle"   100  0.015  4  "exp5_bottle_seed100"
run_experiment "bottle"   2026 0.015  4  "exp6_bottle_seed2026"

# 7-10) 구조적 가설 검증 - screw 집중 (Noise & Epoch)
run_experiment "screw"    0    0.010  4  "exp7_screw_noise010"
run_experiment "screw"    0    0.005  4  "exp8_screw_noise005"
run_experiment "screw"    0    0.015  2  "exp9_screw_epoch2"
run_experiment "screw"    0    0.015  8  "exp10_screw_epoch8"

echo "=========================================================="
echo "🎉 All 10 experiments completed!"
echo "Check results in ${WORK_DIR}/results/ablation/"
echo "=========================================================="
