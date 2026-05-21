#!/usr/bin/env bash
# Reverse Distillation (RD) baseline 실행 — upstream hq-deng/RD4AD 사용
#
# 사용법:
#   CATEGORY=toothbrush MVTEC_DIR=/path/to/mvtec bash run_baseline.sh
#
# 환경변수:
#   CATEGORY      : MVTec AD 카테고리 (default: toothbrush)
#   MVTEC_DIR     : MVTec AD 루트 (default: $HOME/mvtec)
#   RD_DIR        : upstream repo clone 경로 (default: $HOME/RD4AD)

set -euo pipefail

CATEGORY="${CATEGORY:-toothbrush}"
MVTEC_DIR="${MVTEC_DIR:-$HOME/mvtec}"
RD_DIR="${RD_DIR:-$HOME/RD4AD}"

WORK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "[run_baseline] CATEGORY=${CATEGORY}"
echo "[run_baseline] MVTEC_DIR=${MVTEC_DIR}"
echo "[run_baseline] RD_DIR=${RD_DIR}"

# 1) upstream clone (필요 시)
if [ ! -d "$RD_DIR" ]; then
    echo "[run_baseline] cloning upstream into $RD_DIR"
    git clone https://github.com/hq-deng/RD4AD.git "$RD_DIR"
fi

# 2) 데이터셋 링크 (hq-deng/RD4AD는 코드 루트의 'mvtec' 폴더를 기대함)
if [ ! -d "$RD_DIR/mvtec" ]; then
    echo "[run_baseline] linking $MVTEC_DIR to $RD_DIR/mvtec"
    # Windows 환경을 고려하여 ln -s 대신 필요시 처리 (여기서는 일반적인 sh 호환성 유지)
    ln -s "$MVTEC_DIR" "$RD_DIR/mvtec" || cp -r "$MVTEC_DIR" "$RD_DIR/mvtec"
fi

# 3) 실행
cd "$RD_DIR"
# hq-deng/RD4AD의 main.py는 기본적으로 모든 카테고리를 순회하거나 특정 설정을 따름.
# toothbrush만 실행하기 위해 main.py 수정이 필요할 수 있음.
python main.py

echo "[run_baseline] RD execution completed."
