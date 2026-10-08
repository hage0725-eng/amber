"""第二意見：拿任何一份 daily-progress-review 產出的分析檔，用 paiho-core 引擎重判一次。

用法：python tools/check_report.py <T組進度完整分析_MMDD.xlsx> <分析日 YYYY-MM-DD>
==> 一致率 100% 表示報告與共用規則庫同步；有差異就列出，代表 skill 或規則庫其中一邊漂移了。
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
sys.path[:0] = [str(ROOT / "core"), str(ROOT / "dpr"), str(ROOT / "tools")]
from engine import classify_row, resolve_columns  # noqa: E402
from make_golden import find_col, norm_level, norm_risk  # noqa: E402
from paiho_core import load_rules  # noqa: E402


def main(src, day):
    day = dt.date.fromisoformat(day)
    xl = pd.ExcelFile(src)
    sheet = next(s for s in xl.sheet_names if s.startswith("1."))
    df = pd.read_excel(src, sheet_name=sheet, dtype=str, na_filter=False)
    cmap = resolve_columns(df.columns)
    lvl = find_col(df.columns, "異常等級")
    rsk = find_col(df.columns, "風險等級")
    R = load_rules()
    got = [classify_row({k: r[c] for k, c in cmap.items()}, day, R) for _, r in df.iterrows()]
    df["_exp"] = df[lvl].map(norm_level)
    df["_got"] = [g["level"] for g in got]
    df["_exp_r"] = df[rsk].map(norm_risk)
    df["_got_r"] = [g["risk"] for g in got]
    bad = df[(df._exp != df._got) | (df._exp_r != df._got_r)]
    rate = 1 - len(bad) / len(df)
    print(f"規則庫 {R['version']} 對 {Path(src).name}：一致率 {rate:.2%}（{len(df)} 列，不一致 {len(bad)} 列）")
    if len(bad):
        out = Path(src).with_name(Path(src).stem + "_規則差異.csv")
        keep = [cmap["order_no"], cmap["hash"], "_exp", "_got", "_exp_r", "_got_r"]
        bad[keep].to_csv(out, index=False, encoding="utf-8-sig")
        print(f"==> 有漂移，差異明細：{out}")
        return 1
    print("==> 報告與規則庫同步")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    sys.exit(main(*sys.argv[1:3]))
