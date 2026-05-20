#!/usr/bin/env bash
# Reverse Distillation (RD) baseline 실행 — upstream hxcat/ReverseDistillation 사용 권장
#
# 사용법:
#   CATEGORY=toothbrush MVTEC_DIR=/path/to/mvtec bash run_baseline.sh
#
# 환경변수:
#   CATEGORY      : MVTec AD 카테고리 (default: toothbrush)
#   MVTEC_DIR     : MVTec AD 루트 (default: $HOME/mvtec)
#   RD_DIR        : upstream repo clone 경로 (default: $HOME/ReverseDistillation)

set -euo pipefail

CATEGORY="${CATEGORY:-toothbrush}"
MVTEC_DIR="${MVTEC_DIR:-$HOME/mvtec}"
RD_DIR="${RD_DIR:-$HOME/ReverseDistillation}"

WORK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "[run_baseline] CATEGORY=${CATEGORY}"
echo "[run_baseline] MVTEC_DIR=${MVTEC_DIR}"
echo "[run_baseline] RD_DIR=${RD_DIR}"

# 1) upstream clone (필요 시)
if [ ! -d "$RD_DIR" ]; then
    echo "[run_baseline] cloning upstream into $RD_DIR"
    git clone https://github.com/hxcat/Reverse-Distillation.git "$RD_DIR"
fi

# 2) 실행 (기본 설정 사용)
cd "$RD_DIR"
# python main.py --category "$CATEGORY" --data_path "$MVTEC_DIR" ... (구체적인 인자는 upstream 코드 확인 후 조정)

echo "[run_baseline] RD execution logic needs to be finalized after upstream code review."
