"""從 Amber 已確認的「T組進度完整分析_MMDD」產出黃金樣本。

用法：python tools/make_golden.py <分析檔.xlsx> <分析日 YYYY-MM-DD> <標籤> [--force]
已存在的標籤不會被覆蓋，除非加 --force（且須 Amber 同意）。
只保留判定需要的輸入欄＋期望結果，存成 tests/golden/<標籤>.csv.gz。
"""
import datetime as dt
import sys
from pathlib import Path

import pandas as pd

for _s in (sys.stdout, sys.stderr):          # Windows 主控台 cp950/cp1252 也能印中文
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "dpr"))
from engine import resolve_columns  # noqa: E402


def norm_level(s):
    s = str(s)
    for k in ("DELAY", "WARNING", "POTENTIAL"):
        if k in s:
            return k
    if "89" in s and "不列" in s:
        return "EXCLUDED89"
    if s.strip().startswith("OK"):
        return "OK"
    return "UNKNOWN"


def norm_risk(s):
    s = str(s).strip()
    m = {"🔴": "HIGH", "🟠": "MED_HIGH", "🟡": "MEDIUM", "⚪": "LOW"}
    if s[:1] in m:
        return m[s[:1]]
    if s.startswith("OK"):
        return "OK"
    if "DB 89" in s:
        return "NA"
    return "UNKNOWN"


def find_col(columns, key):
    hits = [c for c in columns if key in str(c)]
    if not hits:
        raise SystemExit(f"找不到「{key}」欄，不得臆測，請確認是否為 daily-progress-review 產出的分析檔")
    return hits[0]


def main(src, day, tag, force=False):
    dt.date.fromisoformat(day)          # 日期格式錯就直接報錯
    dst = ROOT / "tests" / "golden" / f"{tag}.csv.gz"
    if dst.exists() and not force:
        raise SystemExit(f"{dst.name} 已存在（已核定的黃金樣本），不覆蓋。確定要換請加 --force")
    xl = pd.ExcelFile(src)
    sheet = next(s for s in xl.sheet_names if s.startswith("1."))
    df = pd.read_excel(src, sheet_name=sheet, dtype=str, na_filter=False)  # 保留 #N/A 原字，不可轉空白
    cmap = resolve_columns(df.columns)
    lvl = find_col(df.columns, "異常等級")
    rsk = find_col(df.columns, "風險等級")
    out = pd.DataFrame({k: df[c] for k, c in cmap.items()})
    out["exp_level"] = df[lvl].map(norm_level)
    out["exp_risk"] = df[rsk].map(norm_risk)
    bad = (out.exp_level == "UNKNOWN").sum()
    if bad:
        raise SystemExit(f"有 {bad} 列異常等級無法辨識，不得臆測，請人工確認")
    out.to_csv(dst, index=False, compression="gzip")
    meta = ROOT / "tests" / "golden" / "manifest.csv"
    rows = pd.read_csv(meta, dtype=str) if meta.exists() else pd.DataFrame(columns=["tag", "date", "source", "rows"])
    rows = rows[rows.tag != tag]
    rows = pd.concat([rows, pd.DataFrame([{"tag": tag, "date": day, "source": Path(src).name, "rows": str(len(out))}])], ignore_index=True)
    rows.sort_values("tag").to_csv(meta, index=False)
    print(f"✅ {dst.name}：{len(out)} 列，分析日 {day}")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--force"]
    if len(args) != 3:
        raise SystemExit(__doc__)
    main(*args, force="--force" in sys.argv)
