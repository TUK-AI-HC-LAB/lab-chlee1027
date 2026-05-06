#!/usr/bin/env bash
# PatchCore baseline 실행 — upstream amazon-science/patchcore-inspection 사용
#
# 사용법:
#   CATEGORY=bottle MVTEC_DIR=/path/to/mvtec bash run_baseline.sh
#
# 환경변수:
#   CATEGORY      : MVTec AD 카테고리 (default: bottle)
#   MVTEC_DIR     : MVTec AD 루트 (default: $HOME/mvtec)
#   PATCHCORE_DIR : upstream repo clone 경로 (default: $HOME/patchcore-inspection)
#   RESULT_NAME   : upstream 안의 결과 폴더 이름 (default: results_${CATEGORY})

set -euo pipefail

CATEGORY="${CATEGORY:-bottle}"
MVTEC_DIR="${MVTEC_DIR:-$HOME/mvtec}"
PATCHCORE_DIR="${PATCHCORE_DIR:-$HOME/patchcore-inspection}"
RESULT_NAME="${RESULT_NAME:-results_${CATEGORY}}"

WORK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "[run_baseline] CATEGORY=${CATEGORY}"
echo "[run_baseline] MVTEC_DIR=${MVTEC_DIR}"
echo "[run_baseline] PATCHCORE_DIR=${PATCHCORE_DIR}"

# 1) upstream clone
if [ ! -d "$PATCHCORE_DIR" ]; then
    echo "[run_baseline] cloning upstream into $PATCHCORE_DIR"
    git clone https://github.com/amazon-science/patchcore-inspection.git "$PATCHCORE_DIR"
fi

# 2) 수정사항 적용
#   2-a) source/run_patchcore.py (수정본 전체 파일)이 있으면 그걸로 덮어쓰기
#   2-b) 없으면 apply_modifications.py로 패치 (idempotent)
if [ -f "${WORK_DIR}/run_patchcore.py" ]; then
    echo "[run_baseline] using local run_patchcore.py (full modified file)"
    cp "${WORK_DIR}/run_patchcore.py" "${PATCHCORE_DIR}/bin/run_patchcore.py"
else
    echo "[run_baseline] applying modifications via apply_modifications.py"
    python "${WORK_DIR}/apply_modifications.py" "${PATCHCORE_DIR}/bin/run_patchcore.py"
fi

# 3) 실행
cd "$PATCHCORE_DIR"
PYTHONPATH=src python bin/run_patchcore.py \
    --gpu 0 \
    --seed 0 \
    --save_patchcore_model \
    --save_segmentation_images \
    "$RESULT_NAME" \
    patch_core \
    -b wideresnet50 \
    -le layer2 \
    -le layer3 \
    --pretrain_embed_dimension 1024 \
    --target_embed_dimension 1024 \
    --anomaly_scorer_num_nn 1 \
    --patchsize 3 \
    sampler \
    -p 0.1 approx_greedy_coreset \
    dataset \
    --resize 256 \
    --imagesize 224 \
    -d "$CATEGORY" \
    mvtec "$MVTEC_DIR"

echo "[run_baseline] done. Results under ${PATCHCORE_DIR}/${RESULT_NAME}/"
echo "[run_baseline] copy metrics csv to: ${WORK_DIR}/results/baseline_${CATEGORY}_$(date +%Y%m%d).csv"
