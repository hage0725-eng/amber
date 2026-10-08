"""回歸守門：修改規則或程式後必跑，全綠才可 commit / 安裝。

用法：python tools/gate.py            （跑全部）
      python tools/gate.py --report   （另輸出不符明細 reports/gate_mismatch.csv）

檢查項：
  G1  rules.yaml 結構完整（必要鍵、門檻合理）
  G2  每份黃金樣本（非 89）異常等級 0 不符
  G3  每份黃金樣本（非 89）風險等級 0 不符
  G4  負向探針：故意改壞 rules.yaml，G2/G3/G6 必須抓到（證明測試有牙齒）
  G5  89 預告列 0 不符
  G8  回填往返：拆檔→模擬回填（含竄改、刪列、未交回、另存）→收回，逐格驗證
  G8b 回填攻擊：舊日期檔、重複檔、「=」文字、清空、與 Amber 衝突、異格式、寫錯列、人名
  G9  閘門 A：4 種正常格式通過、8 種匯出問題停線、重跑與 --accept
  G6  邊界案例：依 tests/approved.yaml（Amber 核定值）生成「剛好達標 / 差一天」的模擬單
      （黃金樣本裡樣品 ≥14 天的單都另有逾期條件，門檻本身測不到，靠這組補）
"""
from __future__ import annotations

import copy
import datetime as dt
import sys
from pathlib import Path

import pandas as pd

for _s in (sys.stdout, sys.stderr):          # Windows 主控台 cp950/cp1252 也能印中文與 ✅
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "core"))
sys.path.insert(0, str(ROOT / "dpr"))
from paiho_core import load_rules  # noqa: E402
from engine import classify_row  # noqa: E402

# 黃金樣本（非 89 列）必須 0 不符；有合理差異請先經 Amber 裁示再重產樣本，不得放寬門檻
GOLDEN = ROOT / "tests" / "golden"
REQUIRED = [
    ("order_class", "sample"), ("order_class", "bulk"), ("order_class", "forecast"),
    ("dpr", "thresholds"), ("dpr", "positive_test"), ("dpr", "forecast_excluded"),
    ("dpr", "priority_suffix"), ("dpr", "yarn_plus_stall_escalate"), ("dpr", "test_result"),
]


def run_golden(rules, tag, day):
    df = pd.read_csv(GOLDEN / f"{tag}.csv.gz", dtype=str, keep_default_na=False)
    got = [classify_row(r, day, rules) for r in df.to_dict("records")]
    df["got_level"] = [g["level"] for g in got]
    df["got_risk"] = [g["risk"] for g in got]
    df["got_reasons"] = [",".join(g["reasons"]) for g in got]
    return df


def _blank_row(**kw):
    r = dict(hash="86", order_no="TEST-1", reply_kh="2026/09/01", sq19="2026/09/30",
             sq_mail="0", yarn="", prog_y="94-C001-1 09/14", prog_t="94-C001-1 09/15",
             changed="是có", test="P", prod_days="5.3", over_std="-", over_1p9="-",
             over_kh="-", reserved="-")
    r.update(kw)
    return r


def load_approved():
    import yaml
    with open(ROOT / "tests" / "approved.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def boundary_cases(R=None):
    """回傳 [(說明, row, today, 期望等級, 期望風險或 None[, 必含原因碼])]。
    門檻取自 tests/approved.yaml（Amber 核定值），不從 rules.yaml 推——否則改壞門檻時邊界也跟著改，測不出來。"""
    A = load_approved()
    day = dt.date(2026, 9, 16)
    th = A["thresholds"]
    pt = A["positive_test"]
    C = []
    for cls, codes in (("sample", A["sample_codes"]), ("bulk", A["bulk_codes"])):
        d, w = th[cls]["delay_days"], th[cls]["warning_days"]
        for code in codes:
            C += [
                (f"#{code} 生產 {d} 天", _blank_row(hash=code, prod_days=f"{d}.3"), day, "DELAY", "MED_HIGH"),
                (f"#{code} 生產 {d-1} 天", _blank_row(hash=code, prod_days=f"{d-1}.3"), day, "WARNING", "MEDIUM"),
                (f"#{code} 生產 {w} 天", _blank_row(hash=code, prod_days=f"{w}.3"), day, "WARNING", "MEDIUM"),
                (f"#{code} 生產 {w-1} 天", _blank_row(hash=code, prod_days=f"{w-1}.3"), day, "OK", "OK"),
            ]
    g = A["grace_days"]
    C += [
        ("寬限：下單≤N天且1.9空白", _blank_row(prod_days=f"{g}.3", sq19="0", reply_kh="0"), day, "OK", "OK"),
        ("寬限外一天", _blank_row(prod_days=f"{g+1}.3", sq19="0", reply_kh="0"), day, "POTENTIAL", "LOW"),
        ("寬限要 1.9 空白才算", _blank_row(prod_days=f"{g}.3", reply_kh="0"), day, "POTENTIAL", "LOW"),
        ("負生產天數不給寬限", _blank_row(prod_days="-1", sq19="0", test="F"), day, "DELAY", "HIGH"),
        ("89 預告不列異常", _blank_row(hash="89", prod_days="40.3"), day, "EXCLUDED89", "NA"),
        ("過1.9＋Mail 未到期", _blank_row(over_1p9="3.3", sq_mail="2026/09/20"), day, "WARNING", "MEDIUM"),
        ("過1.9＋Mail＝今天", _blank_row(over_1p9="3.3", sq_mail="2026/09/16"), day, "WARNING", "MEDIUM"),
        ("過1.9＋Mail 也逾期", _blank_row(over_1p9="3.3", sq_mail="2026/09/10"), day, "DELAY", "MED_HIGH"),
        ("過1.9＋無 Mail", _blank_row(over_1p9="3.3"), day, "DELAY", "MED_HIGH"),
        ("過1.9 不到一天（10/8 起）", _blank_row(over_1p9="0.3"), dt.date(2026, 10, 8),
         "DELAY" if pt["over_1p9"] == "raw" else "OK", None),
        ("過1.9 不到一天（10/7 以前舊口徑）", _blank_row(over_1p9="0.3"), dt.date(2026, 10, 7),
         "DELAY" if A["positive_test_before_1008"]["over_1p9"] == "raw" else "OK", None),
        ("過客戶交期 不到一天", _blank_row(over_kh="0.3"), day,
         "DELAY" if pt["over_kh"] == "raw" else "OK", None),
        ("過客戶交期 3 天", _blank_row(over_kh="3.3"), day, "DELAY", "HIGH"),
        ("過客戶交期欄存成日期", _blank_row(over_kh="2026-09-10 00:00:00"), day, "DELAY", "HIGH"),
        ("過標準交期 不到一天", _blank_row(over_std="0.3"), day,
         "WARNING" if pt["over_std"] == "raw" else "OK", None),
        ("過標準交期 2 天", _blank_row(over_std="2.3"), day, "WARNING", "MEDIUM"),
        ("天數欄是日期序號（未填）", _blank_row(over_kh="46281.34"), day, "OK", "OK"),
        ("測試 F", _blank_row(test="F"), day, "DELAY", "HIGH"),
        ("測試 f 小寫", _blank_row(test="f"), day, "DELAY", "HIGH"),
        ("測試 Q 特採", _blank_row(test="Q"), day, "WARNING", "MEDIUM"),
        ("測試 T", _blank_row(test="T"), day, "POTENTIAL", "LOW"),
        ("測試 0", _blank_row(test="0"), day, "POTENTIAL", "LOW"),
        ("測試 B", _blank_row(test="B"), day, "POTENTIAL", "LOW"),
        ("測試 P 通過", _blank_row(test="P"), day, "OK", "OK"),
        ("保留夠數量", _blank_row(reserved="✔"), day, "WARNING", "MEDIUM"),
        ("缺紗", _blank_row(yarn="✔"), day, "WARNING", "MED_HIGH"),
        ("未回覆客戶", _blank_row(reply_kh="0"), day, "POTENTIAL", "LOW"),
        ("回覆客戶 #N/A＝未回覆", _blank_row(reply_kh="#N/A"), day, "POTENTIAL", "LOW"),
        ("潛在停滯（越文 không）", _blank_row(changed="không"), day, "POTENTIAL", "LOW", "MAYBE_STALL"),
        ("連續停滯", _blank_row(changed="否không", prog_t="94-C001-1 09/14"), day, "POTENTIAL", "LOW", "STALL"),
        ("測試 0.0（Excel 數字）", _blank_row(test="0.0"), day, "POTENTIAL", "LOW", "TEST_0"),
        ("缺紗＋連續停滯 🆘", _blank_row(yarn="✔", changed="否không", prog_t="94-C001-1 09/14"), day, "DELAY", "HIGH"),
        ("缺紗＋兩天進度都空白", _blank_row(yarn="✔", changed="否không", prog_t="", prog_y=""), day, "WARNING", "MED_HIGH"),
        ("DELAY＋過客戶交期", _blank_row(prod_days="20.3", over_kh="2.3"), day, "DELAY", "HIGH"),
    ]
    for code in A["priority_codes"]:
        C += [
            (f"{code} 最優先", _blank_row(order_no=f"ORD-1{code}"), day, "DELAY", "HIGH"),
            (f"{code} 寬限不救", _blank_row(order_no=f"{code}-2609", prod_days=f"{g}.3", sq19="0"), day, "DELAY", "HIGH"),
        ]
    return C


def check_rules(R):
    errs = []
    for a, b in REQUIRED:
        if a not in R or b not in R[a]:
            errs.append(f"缺少 {a}.{b}")
    for k, t in R.get("dpr", {}).get("thresholds", {}).items():
        if not (0 < t["warning_days"] < t["delay_days"]):
            errs.append(f"{k} 門檻不合理：warning {t['warning_days']} 應 < delay {t['delay_days']}")
    for k, v in R.get("dpr", {}).get("positive_test", {}).items():
        if v not in ("raw", "floor"):
            errs.append(f"positive_test.{k}={v} 只能是 raw/floor")
    return errs


def main(report=False, skip_flow=False):
    R = load_rules()
    results = []
    ok_all = True

    errs = check_rules(R)
    results.append(("G1 規則結構", not errs, "; ".join(errs) or f"version {R.get('version')}"))
    ok_all &= not errs

    manifest = pd.read_csv(GOLDEN / "manifest.csv", dtype=str)
    mism = []
    base_bad = {}
    for _, m in manifest.iterrows():
        day = dt.date.fromisoformat(m["date"])
        df = run_golden(R, m["tag"], day)
        core = df[df.hash.str.strip() != "89"]           # 89 自動通過，不計分
        f89 = df[df.hash.str.strip() == "89"]
        bad_l = (core.got_level != core.exp_level).sum()
        bad_r = (core.got_risk != core.exp_risk).sum()
        bad89 = ((f89.got_level != f89.exp_level) | (f89.got_risk != f89.exp_risk)).sum()
        base_bad[m["tag"]] = bad_l + bad_r
        results.append((f"G2 等級 {m['tag']}", bad_l == 0, f"不符 {bad_l} / {len(core)} 列（非 89，須 0）"))
        results.append((f"G3 風險 {m['tag']}", bad_r == 0, f"不符 {bad_r} / {len(core)} 列（須 0）"))
        results.append((f"G5 89 預告 {m['tag']}", bad89 == 0, f"不符 {bad89} / {len(f89)} 列（須 0）"))
        ok_all &= bad_l == 0 and bad_r == 0 and bad89 == 0
        bad = df[(df.got_level != df.exp_level) | (df.got_risk != df.exp_risk)].copy()
        bad.insert(0, "tag", m["tag"])
        mism.append(bad)

    # G6 邊界案例（等級＋風險）
    def case_fail(rules):
        out = []
        for name, row, day, exp, exp_r, *why in boundary_cases():
            g = classify_row(row, day, rules)
            if g["level"] != exp or (exp_r and g["risk"] != exp_r) or (why and why[0] not in g["reasons"]):
                out.append(f"{name}→{g['level']}/{g['risk']}")
        return out

    bfail = case_fail(R)
    results.append(("G6 邊界案例", not bfail, "; ".join(bfail[:6]) or f"{len(boundary_cases())} 例全過"))
    ok_all &= not bfail

    # G4 負向探針：故意改壞 rules.yaml，邊界案例或黃金樣本必須至少抓到一處
    def bump(path, f):
        def mut(r):
            node = r
            for k in path[:-1]:
                node = node[k]
            node[path[-1]] = f(node[path[-1]])
        return mut

    probes = {
        "樣品 DELAY +1": bump(["dpr", "thresholds", "sample", "delay_days"], lambda v: v + 1),
        "樣品 WARNING +1": bump(["dpr", "thresholds", "sample", "warning_days"], lambda v: v + 1),
        "量產 DELAY -1": bump(["dpr", "thresholds", "bulk", "delay_days"], lambda v: v - 1),
        "量產 WARNING -1": bump(["dpr", "thresholds", "bulk", "warning_days"], lambda v: v - 1),
        "寬限 +1": bump(["dpr", "grace_days"], lambda v: v + 1),
        "85 移出樣品": bump(["order_class", "sample"], lambda v: [c for c in v if c != "85"]),
        "87 移出樣品": bump(["order_class", "sample"], lambda v: [c for c in v if c != "87"]),
        "過客戶交期 raw↔floor": bump(["dpr", "positive_test", "over_kh"], lambda v: "floor" if v == "raw" else "raw"),
        "過標準交期 raw↔floor": bump(["dpr", "positive_test", "over_std"], lambda v: "floor" if v == "raw" else "raw"),
        "過1.9 raw↔floor": bump(["dpr", "positive_test", "over_1p9"], lambda v: "floor" if v == "raw" else "raw"),
        "Q 改成 POTENTIAL": lambda r: (r["dpr"]["test_result"]["warning"].remove("Q"),
                                       r["dpr"]["test_result"]["potential"].append("Q")),
        "拿掉 F": lambda r: r["dpr"]["test_result"]["delay"].remove("F"),
        "拿掉 T": lambda r: r["dpr"]["test_result"]["potential"].remove("T"),
        "取消 KN": lambda r: r["dpr"]["priority_suffix"]["suffixes"].pop("KN"),
        "取消 LL": lambda r: r["dpr"]["priority_suffix"]["suffixes"].pop("LL"),
        "取消 XLBT": lambda r: r["dpr"]["priority_suffix"]["suffixes"].pop("XLBT"),
        "最優先改成尾碼比對": bump(["dpr", "priority_suffix", "match"], lambda v: "endswith"),
        "89 改回列異常": bump(["dpr", "forecast_excluded", "effective_from"], lambda v: "2099-01-01"),
        "🆘 停用": bump(["dpr", "yarn_plus_stall_escalate", "effective_from"], lambda v: "2099-01-01"),
        "刪掉 過1.9 舊口徑": lambda r: r["dpr"].__setitem__("positive_test_history", []),
    }
    for name, mut in probes.items():
        R2 = copy.deepcopy(R)
        mut(R2)
        caught = bool(case_fail(R2))
        for _, m in ([] if caught else manifest.iterrows()):
            df = run_golden(R2, m["tag"], dt.date.fromisoformat(m["date"]))
            if ((df.got_level != df.exp_level) | (df.got_risk != df.exp_risk)).sum() > 0:
                caught = True
                break
        results.append((f"G4 探針 {name}", caught, "有抓到" if caught else "⚠️ 測試沒反應＝沒牙齒"))
        ok_all &= caught

    # G8 / G9 自動化流程（回填往返、閘門 A）；hook 改到非 flow 檔時可略過以省時間
    if not skip_flow:
        sys.path.insert(0, str(ROOT / "tests"))
        import flow_attacks
        import flow_roundtrip
        import intake_test
        for name, mod in (("G8 回填往返", flow_roundtrip), ("G8b 回填攻擊", flow_attacks),
                          ("G9 閘門A 原檔健檢", intake_test)):
            try:
                ok, note = mod.run()
            except Exception as e:          # 測試本身壞掉也算紅燈
                ok, note = False, f"測試執行錯誤：{e!r}"[:300]
            results.append((name, ok, note))
            ok_all &= ok
    else:
        results.append(("G8/G9 流程測試", True, "本次略過（--skip-flow）"))

    # G7 裁示登錄表：已裁示但未落地＝「決議沒交付」，列出提醒（不擋 commit）
    dec = pd.read_csv(ROOT / "core" / "decisions.csv", dtype=str, keep_default_na=False)
    pending = dec[dec.status == "待裁示"]
    undelivered = dec[dec.status == "已裁示"]
    note = f"待裁示 {len(pending)}｜已裁示未落地 {len(undelivered)}"
    if len(undelivered):
        note += "：" + "、".join(undelivered.id)
    results.append(("G7 裁示登錄（提醒）", True, note))

    w = max(len(r[0]) for r in results)
    print("=" * 60)
    for name, ok, note in results:
        print(f"{'✅' if ok else '❌'} {name.ljust(w)}  {note}")
    print("=" * 60)
    print("==> 全綠，可交付" if ok_all else "==> 有紅燈，不可 commit / 安裝")

    if report and mism:
        out = ROOT / "reports"
        out.mkdir(exist_ok=True)
        pd.concat(mism).to_csv(out / "gate_mismatch.csv", index=False, encoding="utf-8-sig")
        print(f"不符明細：{out / 'gate_mismatch.csv'}")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main(report="--report" in sys.argv, skip_flow="--skip-flow" in sys.argv))
