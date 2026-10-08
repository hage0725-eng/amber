#!/bin/sh
# paiho-workflow 安裝（macOS / Linux / Git Bash）
set -e
cd "$(dirname "$0")"
export PYTHONUTF8=1 PYTHONIOENCODING=utf-8
PY=python3; command -v python3 >/dev/null 2>&1 || PY=python
command -v git >/dev/null 2>&1 || { echo "缺少 git"; exit 1; }
echo "1/4 安裝 Python 套件..."; $PY -m pip install --user -q -r requirements.txt 2>/dev/null || $PY -m pip install --user -q --break-system-packages -r requirements.txt
echo "2/4 建立版本控管..."; [ -d .git ] || git init -q -b main; git config core.hooksPath .githooks; printf '%s' "$(command -v $PY)" > .githooks/python_path
echo "3/4 跑回歸守門..."; $PY tools/gate.py || { echo "==> gate 紅燈，安裝中止"; exit 1; }
echo "4/4 首次提交..."; git add -A; git -c user.name="Amber Lin" -c user.email="hage0725@gmail.com" commit -q -m "paiho-workflow 初版：共用規則庫＋DPR 回歸守門" || { echo "==> 提交失敗"; exit 1; }
echo "==> 安裝完成。在本資料夾執行 claude，輸入 /gate 試跑。"
