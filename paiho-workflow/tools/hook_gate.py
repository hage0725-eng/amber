"""Claude Code PostToolUse hook：改到規則或程式就自動跑 gate。

紅燈時以 exit code 2 回報，Claude 會看到錯誤並必須先修好。
只在改到 core/、dpr/、tools/、tests/、flow/ 時觸發，其他檔案不浪費時間。
"""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WATCH = ("core", "dpr", "tools", "tests", "flow")


def main():
    raw = sys.stdin.buffer.read()
    try:
        data = json.loads(raw.decode("utf-8"))
    except Exception:
        # 讀不懂輸入時寧可跑一次 gate，也不要默默放行
        data = {"tool_input": {"file_path": str(ROOT / "core" / "rules.yaml")}}
    if not isinstance(data, dict):
        return 0
    fp = (data.get("tool_input") or {}).get("file_path") or ""
    try:
        rel = Path(fp).resolve().relative_to(ROOT)
    except Exception:
        return 0
    if not rel.parts or rel.parts[0] not in WATCH:
        return 0
    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    args = [sys.executable, str(ROOT / "tools" / "gate.py")]
    flow_related = rel.parts[0] in ("flow", "tests") or rel.as_posix() in ("core/paiho_core.py", "core/rules.yaml")
    if not flow_related:
        args.append("--skip-flow")          # 與自動化流程無關的改動略過約 2 分鐘的流程測試；commit 時仍全跑
    r = subprocess.run(args,
                       capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    if r.returncode != 0:
        try:
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
        sys.stderr.write(f"gate 紅燈（改動：{rel}），先修好再繼續：\n{r.stdout[-3000:]}")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
