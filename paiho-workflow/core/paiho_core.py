"""paiho-core：共用規則載入與共用小工具。

所有 skill / 腳本都從這裡取規則，不得在自己的程式裡寫死門檻。
"""
from __future__ import annotations

import datetime as dt
import math
from functools import lru_cache
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
RULES_PATH = ROOT / "rules.yaml"
EXCEL_EPOCH = dt.date(1899, 12, 30)


@lru_cache(maxsize=4)
def load_rules(path: str | None = None) -> dict:
    p = Path(path) if path else RULES_PATH
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _isna(v) -> bool:
    try:
        import pandas as pd
        return bool(pd.isna(v)) if not isinstance(v, (list, tuple, dict)) else False
    except (TypeError, ValueError):
        return False


def to_float(v):
    """把 '-'、空白、#N/A、NaT、inf 等轉成 None；數字照轉。"""
    if v is None or _isna(v):
        return None
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        f = float(v)
    else:
        s = str(v).strip()
        if s in ("", "-", "nan", "None", "#N/A", "NaT"):
            return None
        try:
            f = float(s)
        except ValueError:
            return None
    return f if math.isfinite(f) else None


def to_date(v):
    """'2026/09/16'、datetime、Excel 序號 → date；'0'/空白 → None（=未填）。"""
    if v is None or _isna(v):
        return None
    if isinstance(v, dt.datetime):
        return v.date()
    if isinstance(v, dt.date):
        return v
    s = str(v).strip()
    if s in ("", "0", "0.0", "-", "nan", "None", "NaT", "00:00:00"):
        return None
    for fmt in ("%Y/%m/%d", "%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y/%m/%d %H:%M:%S",
                "%Y-%m-%dT%H:%M:%S", "%m/%d/%Y"):
        try:
            return dt.datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    f = to_float(s)
    if f is not None and 365 < f < 2958466:   # 2958466 = 9999-12-31
        return EXCEL_EPOCH + dt.timedelta(days=int(f))
    return None


def looks_like_date(v) -> bool:
    """天數欄被誤存成日期格式（datetime 或 '2026-09-05 00:00:00'）時用。"""
    if v is None or _isna(v):
        return False
    if isinstance(v, (dt.date, dt.datetime)):
        return True
    s = str(v or "").strip()
    return len(s) >= 8 and ("/" in s or "-" in s[1:]) and to_float(s) is None and to_date(s) is not None


def order_class(hash_code, rules: dict | None = None) -> str:
    r = (rules or load_rules())["order_class"]
    code = str(hash_code).strip().split(".")[0]
    for k in ("sample", "bulk", "forecast"):
        if code in r[k]:
            return k
    return "other"


def station(progress_text, rules: dict | None = None):
    """今日進度 '94-C001-1 09/15 ...' → ('94', '染色', '1')；查不到回 None 不臆測。"""
    r = (rules or load_rules())["dpr"]["process_station"]["codes"]
    s = str(progress_text or "").strip()
    if len(s) < 2 or not s[:2].isdigit():
        return None
    code = s[:2]
    if code not in r:
        return (code, "待確認", None)
    head = s.split()[0]
    suffix = head.rsplit("-", 1)[-1] if head.count("-") >= 2 else None
    return (code, r[code], suffix)
