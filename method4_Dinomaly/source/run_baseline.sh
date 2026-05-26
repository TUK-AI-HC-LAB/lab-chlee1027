#!/usr/bin/env bash

set -euo pipefail

# Method 4: Dinomaly 실험 자동화 스크립트
# 사용법: CATEGORY=bottle MVTEC_DIR=/path/to/mvtec bash run_baseline.sh

if [ -z "${CATEGORY:-}" ]; then
    echo "❌ [오류] CATEGORY 환경변수가 설정되지 않았습니다. (예: CATEGORY=bottle)"
    exit 1
fi

if [ -z "${MVTEC_DIR:-}" ]; then
    echo "❌ [오류] MVTEC_DIR 환경변수가 설정되지 않았습니다. (예: MVTEC_DIR=/path/to/mvtec)"
    exit 1
fi

REPO_DIR="Dinomaly_repo"
MAIN_SCRIPT="dinomaly_mvtec_uni.py"

# 1. 레포지토리 클론 (없을 경우)
if [ ! -d "$REPO_DIR" ]; then
    echo "🚀 공식 Dinomaly 레포지토리를 클론합니다..."
    git clone https://github.com/guojiajeremy/Dinomaly.git "$REPO_DIR"
fi

cd "$REPO_DIR"

# 2. 소스 패치 (idempotent하게 적용)
echo "🛠 소스 패치를 적용합니다..."

# [utils.py] pd.concat 패치
python3 -c "
import pandas as pd
path = 'utils.py'
with open(path, 'r') as f: content = f.read()
old = 'df = df.append({\"pro\": mean(pros), \"fpr\": fpr, \"threshold\": th}, ignore_index=True)'
new = 'new_row = pd.DataFrame([{\"pro\": mean(pros), \"fpr\": fpr, \"threshold\": th}]); df = pd.concat([df, new_row], ignore_index=True)'
if old in content:
    with open(path, 'w') as f: f.write(content.replace(old, new))
    print('✅ utils.py 패치 완료')
"

# [main] CUDA 및 item_list 패치
python3 -c "
import re
path = '$MAIN_SCRIPT'
with open(path, 'r') as f: content = f.read()
content = content.replace(\"device = 'cuda:1'\", \"device = 'cuda:0' if torch.cuda.is_available() else 'cpu'\")
pattern = r\"item_list\\s*=\\s*\\[[^\\]]*\\]\"
content = re.sub(pattern, \"item_list = ['$CATEGORY']\", content, flags=re.DOTALL)
with open(path, 'w') as f: f.write(content)
print('✅ $MAIN_SCRIPT 패치 완료 (Category: $CATEGORY)')
"

# 3. 실험 실행
echo "🧪 실험을 시작합니다: $CATEGORY"
python3 "$MAIN_SCRIPT" --data_path "$MVTEC_DIR" --save_name "baseline_$CATEGORY"

echo "✅ 실험 완료."
