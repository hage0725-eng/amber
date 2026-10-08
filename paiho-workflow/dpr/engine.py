"""daily-progress-review 判定核心。

輸入：1.主分析 的原始欄位（一列一單），以及分析日 today。
輸出：異常等級 DELAY / WARNING / POTENTIAL / OK / EXCLUDED89，
      風險等級 HIGH / MED_HIGH / MEDIUM / LOW / OK / NA，以及原因代碼。
所有門檻一律來自 core/rules.yaml。
"""
from __future__ import annotations

import datetime as dt
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "core"))
from paiho_core import EXCEL_EPOCH, load_rules, looks_like_date, order_class, to_date, to_float  # noqa: E402

# 欄位：只用中文前綴比對，容忍各版表頭的越文 / 換行差異
COLS = {
    "hash": "#",
    "order_no": "訂單號碼",
    "reply_kh": "回復客戶",
    "sq19": "生管回覆 1.9",
    "sq_mail": "生管回覆 Mail",
    "yarn": "缺紗",
    "prog_y": "昨日進度",
    "prog_t": "今日進度",
    "changed": "進度狀況是否更動",
    "test": "測試結果",
    "prod_days": "生產天數",
    "over_std": "過標準交期天數",
    "over_1p9": "過1.9交期天數",
    "over_kh": "過客人交期天數",
    "reserved": "保留夠數量",
}


def resolve_columns(columns) -> dict:
    out = {}
    for key, prefix in COLS.items():
        hits = [c for c in columns if str(c).replace("\n", " ").strip().lstrip("【").startswith(prefix)]
        if key == "hash":
            hits = [c for c in columns if str(c).strip() == "#"]
        if key == "prog_y":
            hits = [c for c in columns if "昨日進度" in str(c)]
        if not hits:
            raise KeyError(f"找不到欄位：{prefix}（不得臆測，請確認表頭）")
        out[key] = hits[0]
    return out


def _days_or_serial(v, today: dt.date, cutoff: float, mode: str = "raw"):
    """天數欄：> cutoff 視為 Excel 日期序號，反推逾期天數；未逾期回 None。
    mode=raw：原值 > 0 即算逾期；mode=floor：取整後 > 0 才算。"""
    if mode not in ("raw", "floor"):
        raise ValueError(f"positive_test 只接受 raw / floor，收到 {mode!r}")
    if looks_like_date(v):            # 天數欄被存成日期格式 → 當日期反推
        d = to_date(v)
        diff = (today - d).days
        return float(diff) if diff > 0 else None
    f = to_float(v)
    if f is None:
        return None
    if f > cutoff:
        d = EXCEL_EPOCH + dt.timedelta(days=int(f))
        diff = (today - d).days
        return float(diff) if diff > 0 else None
    if mode == "floor":
        return float(math.floor(f)) if math.floor(f) > 0 else None
    return f if f > 0 else None


def _blank(v) -> bool:
    if v is None:
        return True
    if isinstance(v, float) and math.isnan(v):
        return True
    return str(v).strip() in ("", "0", "0.0", "-", "#N/A", "nan", "None", "NaT", "00:00:00")


def _tick(v) -> bool:
    return "✔" in str(v or "")


def classify_row(row: dict, today: dt.date, rules: dict | None = None) -> dict:
    R = rules or load_rules()
    D = R["dpr"]
    cls = order_class(row["hash"], R)

    fx = D["forecast_excluded"]
    if cls == "forecast" and today >= _as_date(fx["effective_from"]):
        return {"level": "EXCLUDED89", "risk": "NA", "reasons": [fx["id"]]}

    cutoff = D["serial_cutoff"]
    prod = to_float(row["prod_days"])
    prod_i = math.floor(prod) if prod is not None else None
    pt = dict(D["positive_test"])
    for h in D.get("positive_test_history", []):       # 舊口徑：分析日 ≤ until 時沿用
        if today <= _as_date(h["until"]):
            pt[h["field"]] = h["mode"]
    over_std = _days_or_serial(row["over_std"], today, cutoff, pt["over_std"])
    over_1p9 = _days_or_serial(row["over_1p9"], today, cutoff, pt["over_1p9"])
    over_kh = _days_or_serial(row["over_kh"], today, cutoff, pt["over_kh"])
    mail = to_date(row["sq_mail"])
    test = str(row["test"] if row["test"] is not None else "").strip()
    if test in ("nan", "None"):
        test = ""
    test = test.split(".")[0].upper()
    yarn = _tick(row["yarn"])
    reserved = _tick(row["reserved"])
    no_update = any(k in str(row["changed"] or "") for k in ("否", "không"))
    # 連續停滯＝今日進度與昨日進度「都有值且相同」；兩邊都空白只算潛在停滯
    pt_, py_ = str(row["prog_t"] or "").strip(), str(row["prog_y"] or "").strip()
    prog_same = pt_ != "" and pt_ not in ("nan", "None") and pt_ == py_
    no_reply = _blank(row["reply_kh"])
    sq19_blank = _blank(row["sq19"])

    reasons: list[str] = []
    delay = warning = potential = False
    th = D["thresholds"].get(cls)

    if th and prod_i is not None:
        if prod_i >= th["delay_days"]:
            delay = True
            reasons.append(f"PROD>={th['delay_days']}")
        elif prod_i >= th["warning_days"]:
            warning = True
            reasons.append(f"PROD>={th['warning_days']}")

    s1p9 = None
    if over_1p9 is not None:
        if mail is None or today > mail:
            s1p9 = "delay"
            delay = True
            reasons.append("OVER_1P9")
        else:
            s1p9 = "not_delay"
            warning = True
            reasons.append("OVER_1P9_MAIL_OK")
    if over_kh is not None:
        delay = True
        reasons.append("OVER_KH")
    if test in D["test_result"]["delay"]:
        delay = True
        reasons.append("TEST_F")
    if over_std is not None:
        warning = True
        reasons.append("OVER_STD")
    if test in D["test_result"]["warning"]:
        warning = True
        reasons.append("TEST_Q")
    if yarn:
        warning = True
        reasons.append("YARN")
    if reserved:
        warning = True
        reasons.append("RESERVED")
    if no_update:
        potential = True
        reasons.append("STALL" if prog_same else "MAYBE_STALL")
    if no_reply:
        potential = True
        reasons.append("NO_REPLY")
    if test in D["test_result"]["potential"]:
        potential = True
        reasons.append(f"TEST_{test}")

    level = "DELAY" if delay else "WARNING" if warning else "POTENTIAL" if potential else "OK"

    grace = prod_i is not None and 0 <= prod_i <= D["grace_days"] and sq19_blank
    order_no = str(row["order_no"] or "").strip().upper()
    P = D["priority_suffix"]
    prio = None
    if today >= _as_date(P["effective_from"]):
        hit = (lambda s: s in order_no) if P["match"] == "contains" else (lambda s: order_no.endswith(s))
        prio = next((s for s in P["suffixes"] if hit(s)), None)
    S = D["yarn_plus_stall_escalate"]
    sos = today >= _as_date(S["effective_from"]) and yarn and no_update and prog_same
    if prio or sos:
        level = "DELAY"

    if grace and not (prio or sos):
        level = "OK"
        reasons.append("GRACE")

    # 風險
    if prio or sos:
        risk = "HIGH"
        reasons.append(f"PRIO_{prio}" if prio else "SOS")
    elif level == "DELAY" and (over_kh is not None or yarn or test == "F"):
        risk = "HIGH"
    elif level == "DELAY" or (level == "WARNING" and yarn):
        risk = "MED_HIGH"
    elif level == "WARNING":
        risk = "MEDIUM"
    elif level == "POTENTIAL":
        risk = "LOW"
    else:
        risk = "OK"
    return {"level": level, "risk": risk, "reasons": reasons, "s1p9": s1p9}


def _as_date(v):
    return v if isinstance(v, dt.date) else dt.date.fromisoformat(str(v))


def classify_frame(df, today: dt.date, rules: dict | None = None):
    import pandas as pd

    cmap = resolve_columns(df.columns)
    recs = []
    for _, r in df.iterrows():
        row = {k: r[c] for k, c in cmap.items()}
        recs.append(classify_row(row, today, rules))
    return pd.DataFrame(recs, index=df.index)
