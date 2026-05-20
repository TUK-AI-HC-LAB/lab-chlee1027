#!/usr/bin/env bash
# SimpleNet baseline 실행 — upstream DonaldRR/SimpleNet 사용
#
# 사용법:
#   CATEGORY=bottle MVTEC_DIR=/path/to/mvtec bash run_baseline.sh
#
# 환경변수:
#   CATEGORY      : MVTec AD 카테고리 (default: bottle)
#   MVTEC_DIR     : MVTec AD 루트 (default: $HOME/mvtec)
#   SIMPLENET_DIR : upstream repo clone 경로 (default: $HOME/SimpleNet)
#   RUN_NAME      : upstream 결과 폴더 안 run 이름 (default: ${CATEGORY}_visual)

set -euo pipefail

CATEGORY="${CATEGORY:-bottle}"
MVTEC_DIR="${MVTEC_DIR:-$HOME/mvtec}"
SIMPLENET_DIR="${SIMPLENET_DIR:-$HOME/SimpleNet}"
RUN_NAME="${RUN_NAME:-${CATEGORY}_visual}"

WORK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "[run_baseline] CATEGORY=${CATEGORY}"
echo "[run_baseline] MVTEC_DIR=${MVTEC_DIR}"
echo "[run_baseline] SIMPLENET_DIR=${SIMPLENET_DIR}"

# 1) upstream clone
if [ ! -d "$SIMPLENET_DIR" ]; then
    echo "[run_baseline] cloning upstream into $SIMPLENET_DIR"
    git clone https://github.com/DonaldRR/SimpleNet.git "$SIMPLENET_DIR"
fi

# 2) 수정사항 적용 (idempotent)
#   2-a) metrics.py : pandas 2.0+ 호환 (df.append() 제거 대응)
#   2-b) main.py    : 주석 처리된 test() 호출 활성화 + train() 후 자동 시각화
python - "$SIMPLENET_DIR" <<'PYEOF'
import sys
from pathlib import Path

root = Path(sys.argv[1])

# 2-a) metrics.py
m = root / "metrics.py"
t = m.read_text()
old = 'df = df.append({"pro": np.mean(pros), "fpr": fpr, "threshold": th}, ignore_index=True)'
new = 'df.loc[len(df)] = {"pro": np.mean(pros), "fpr": fpr, "threshold": th}'
if old in t:
    m.write_text(t.replace(old, new))
    print("[patch] metrics.py: df.append -> df.loc")
elif new in t:
    print("[patch] metrics.py: already patched")
else:
    print("[patch] metrics.py: target line not found (upstream may have changed)")

# 2-b) main.py : 시각화(test) 호출 활성화 — upstream 버전에 따라 수동 확인 필요
#   기본 upstream은 train() 내부에서 평가는 수행하나 segmentation 저장 호출이
#   주석 처리되어 있을 수 있음. 활성화 패턴이 환경마다 달라 여기서는 알림만 출력.
print("[patch] main.py: --save_segmentation_images 플래그로 시각화 저장 (코드 패치 필요 시 README 참고)")
PYEOF

# 3) 실행 (논문 동일 설정: WRN-50 layer2+3, embed 1536, resize 329 / imagesize 288, batch 8)
cd "$SIMPLENET_DIR"
python3 main.py \
    --gpu 0 \
    --seed 0 \
    --log_group simplenet_mvtec \
    --log_project MVTecAD_Results \
    --results_path results \
    --run_name "$RUN_NAME" \
    --save_segmentation_images \
    net \
    -b wideresnet50 \
    -le layer2 \
    -le layer3 \
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
    --resize 329 \
    --imagesize 288 \
    -d "$CATEGORY" \
    mvtec "$MVTEC_DIR"

echo "[run_baseline] done. Results under ${SIMPLENET_DIR}/results/MVTecAD_Results/simplenet_mvtec/${RUN_NAME}/"
echo "[run_baseline] copy metrics csv to: ${WORK_DIR}/results/baseline_${CATEGORY}.csv"
