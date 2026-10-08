"""比對 build_dpr.py 過1.9 判定（現行／R-1008-1 修正後）與規則庫引擎。用法：python specs/verify/verify_1p9.py <paiho-workflow 資料夾>"""
import datetime as dt, math, re, sys
from pathlib import Path
import pandas as pd
PW = Path(sys.argv[1]); sys.path[:0] = [str(PW / "core"), str(PW / "dpr")]
from paiho_core import load_rules
from engine import _days_or_serial

ILLEGAL = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f]')
def dnz(x):                      # 照抄 build_dpr.py
    if x is None: return ''
    if isinstance(x, float): return '' if math.isnan(x) else (str(int(x)) if x == int(x) else str(x))
    return ILLEGAL.sub('', str(x).strip())
def fnum(v):
    try:
        f = float(v); return 0.0 if math.isnan(f) else f
    except Exception: return 0.0
def erp_days(v):
    s = dnz(v)
    if s == '-': return ('ontime', None)
    if s in ('', '0'): return ('no_base', None)
    f = fnum(v)
    if f > 365: return ('no_base', None)
    if f > 0: return ('over', math.floor(f))
    return ('ontime', None)

R1008_1_FROM = dt.date(2026, 10, 8)
def hit_old(v, today):
    st, d = erp_days(v); return st == 'over' and (d or 0) > 0
def hit_new(v, today):
    st, d = erp_days(v); return st == 'over' and (today >= R1008_1_FROM or (d or 0) > 0)

R = load_rules(); D = R["dpr"]
def hit_engine(v, today):
    pt = dict(D["positive_test"])
    for h in D.get("positive_test_history", []):
        if today <= dt.date.fromisoformat(str(h["until"])): pt[h["field"]] = h["mode"]
    return _days_or_serial(v, today, D["serial_cutoff"], pt["over_1p9"]) is not None

vals = []
for tag in ("0818", "0916"):
    vals += list(pd.read_csv(PW / "tests/golden" / f"{tag}.csv.gz", dtype=str, keep_default_na=False).over_1p9)
vals = [v for v in vals if not (pd.to_numeric(v, errors="coerce") > 365)]   # 舊檔的 TODAY() 退化序號換日後會變成「過去日期」，不是真逾期
vals += ["0.38", "0.0001", "0.99", "1.2", "3", "-", "", "0", "-0.5", "46302.38", "46303.38"]   # 46302／46303＝10/7、10/8 當天退化序號
print(f"共 {len(vals)} 個過1.9 值")
for day in (dt.date(2026, 10, 7), dt.date(2026, 10, 8), dt.date(2026, 10, 9)):
    eng = [hit_engine(v, day) for v in vals]
    old = [hit_old(v, day) for v in vals]
    new = [hit_new(v, day) for v in vals]
    d_old = sum(a != b for a, b in zip(eng, old)); d_new = sum(a != b for a, b in zip(eng, new))
    ex = sorted({v for v, a, b in zip(vals, eng, new) if a != b})[:5]
    print(f"{day}：現行 builder 不一致 {d_old}｜修正後不一致 {d_new} {ex if ex else ''}｜修正後逾期筆數 {sum(new)}")
