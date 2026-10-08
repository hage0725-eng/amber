"""閘門 A 測試：用 0916 主分析的原始欄位造一份模擬「統整」原檔，
先跑一次正常通過建立基準，再逐一注入常見的匯出問題，每一種都必須停線。
⚠️ 模擬檔，不是真實 ERP 原檔；拿到班長的真實檔後要再校準一次門檻。
"""
from __future__ import annotations

import contextlib
import datetime as dt
import io
import os
import shutil
import sys
import tempfile
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "flow"))
import intake  # noqa: E402

FIXTURE = ROOT / "tests" / "fixtures" / "T組進度完整分析_0916.xlsx"


def _raw():
    df = pd.read_excel(FIXTURE, sheet_name="1.主分析 Phân tích chính", dtype=object)
    df = df.iloc[:, :47]
    df.columns = [str(c).replace(" ", "\n", 1) for c in df.columns]   # 還原 ERP 表頭換行
    oc = [c for c in df.columns if str(c).startswith("訂單號碼")][0]
    parts = []
    for k in range(40):                                                # 放大到約 2,300 列，每份單號不同
        d = df.copy()
        d[oc] = d[oc].astype(str) + f"-{k}"
        parts.append(d)
    return pd.concat(parts, ignore_index=True)


def _write(df, path, sheet="統整", age_h=0.5, now=None):
    with pd.ExcelWriter(path) as w:
        df.to_excel(w, sheet_name=sheet, index=False)
    t = (now - dt.timedelta(hours=age_h)).timestamp()
    os.utime(path, (t, t))


def run():
    tmp = Path(tempfile.mkdtemp(prefix="intake_"))
    now = dt.datetime(2026, 10, 8, 9, 45)
    try:
        base = _raw()
        state = tmp / "state"
        f0 = tmp / "d0.xlsx"
        _write(base, f0, now=now - dt.timedelta(days=1))
        with contextlib.redirect_stdout(io.StringIO()):
            ok0, _ = intake.check(f0, state, now - dt.timedelta(days=1))
        if not ok0:
            return False, "正常檔沒通過（基準建立失敗）"

        oc = [c for c in base.columns if str(c).startswith("訂單號碼")][0]
        ac = [c for c in base.columns if str(c).startswith("助理")][0]
        pc = [c for c in base.columns if str(c).startswith("生產天數")][0]
        good = base.copy()
        good.iloc[0, 1] = "changed"        # 內容不同於基準
        cases = {
            "正常（應通過）": (good, {}, True),
            "缺助理欄": (good.drop(columns=[ac]), {}, False),
            "筆數少 30%": (good.iloc[: int(len(good) * 0.7)], {}, False),
            "空白訂單號 3%": (good.assign(**{oc: [None if i % 33 == 0 else v for i, v in enumerate(good[oc])]}), {}, False),
            "生產天數變文字": (good.assign(**{pc: "abc"}), {}, False),
            "分頁名稱不對": (good, {"sheet": "Sheet1"}, False),
            "昨天的舊檔": (good, {"age_h": 20}, False),
            "與上次同一份": (base, {"age_h": 0.5}, False),
        }
        cases.update({
            "表頭在第 3 列（應通過）": (good, {"pad": 2}, True),
            "缺 #2 欄": (good.drop(columns=["#2"]), {}, False),
            "缺 # 欄但有 # Nét": (good.drop(columns=["#"])[[c for c in good.columns if c.startswith("#\n")]
                                    + [c for c in good.columns if c != "#" and not c.startswith("#\n")]], {}, False),
            "存成 .xls（應通過）": (good, {"fmt": "xls"}, True),
            "ERP 匯出 HTML 偽 .XLS（應通過）": (good, {"fmt": "html"}, True),
        })
        fails = []
        for name, (df, kw, expect) in cases.items():
            st = tmp / f"st_{abs(hash(name))}"
            shutil.copytree(state, st)
            f = tmp / f"{abs(hash(name))}.xlsx"
            if name == "與上次同一份":
                shutil.copy(f0, f)
                t = (now - dt.timedelta(hours=0.5)).timestamp()
                os.utime(f, (t, t))
            else:
                fmt, pad = kw.pop("fmt", None), kw.pop("pad", 0)
                if pad:
                    f = tmp / f"{abs(hash(name))}.xlsx"
                    with pd.ExcelWriter(f) as w:
                        pd.DataFrame([["T組追蹤進度表"], [""]]).to_excel(w, sheet_name="統整", index=False, header=False)
                        df.to_excel(w, sheet_name="統整", index=False, startrow=pad)
                    t = (now - dt.timedelta(hours=0.5)).timestamp()
                    os.utime(f, (t, t))
                elif fmt == "html":
                    f = tmp / f"{abs(hash(name))}.XLS"
                    f.write_text(df.to_html(index=False), encoding="utf-8")
                    t = (now - dt.timedelta(hours=0.5)).timestamp()
                    os.utime(f, (t, t))
                elif fmt == "xls":
                    _write(df, f, now=now, **kw)
                    import subprocess
                    if not shutil.which("soffice"):
                        continue
                    subprocess.run(["soffice", "--headless", "--convert-to", "xls", "--outdir", str(tmp), str(f)],
                                   capture_output=True, timeout=180)
                    f = f.with_suffix(".xls")
                    t = (now - dt.timedelta(hours=0.5)).timestamp()
                    os.utime(f, (t, t))
                else:
                    _write(df, f, now=now, **kw)
            with contextlib.redirect_stdout(io.StringIO()):
                ok, _ = intake.check(f, st, now)
            if ok != expect:
                fails.append(f"{name}→{'通過' if ok else '停線'}")
        # 同日重跑同一份：通過且不洗掉基準；Drive 的 UTC 時間（Z）要能正確換算
        st = tmp / "st_rerun"
        shutil.copytree(state, st)
        f1 = tmp / "rerun.xlsx"
        _write(good, f1, now=now)
        with contextlib.redirect_stdout(io.StringIO()):
            a, _ = intake.check(f1, st, now)
            b, _ = intake.check(f1, st, now + dt.timedelta(minutes=20))
            z, _ = intake.check(f1, st, "2026-10-08T03:05:00Z", "2026-10-08T02:30:00Z")
        if not (a and b and z):
            fails.append(f"同日重跑/UTC 時間：{a},{b},{z}")
        # 筆數大幅變動經 Amber --accept 後放行
        st = tmp / "st_acc"
        shutil.copytree(state, st)
        f2 = tmp / "acc.xlsx"
        _write(good.iloc[: int(len(good) * 0.7)], f2, now=now)
        with contextlib.redirect_stdout(io.StringIO()):
            no, _ = intake.check(f2, st, now)
            yes, _ = intake.check(f2, st, now, accept=True)
        if no or not yes:
            fails.append("--accept 行為不對")
        if fails:
            return False, "；".join(fails)
        n_fail = sum(1 for _df, _kw, e in cases.values() if not e)
        return True, (f"{len(cases) + 2} 種情境全對（{len(cases) - n_fail} 種正常格式通過、{n_fail} 種異常停線、"
                      f"重跑與 --accept 正確）｜模擬檔，待真實原檔校準")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    ok, msg = run()
    print(("✅ " if ok else "❌ ") + msg)
    sys.exit(0 if ok else 1)
