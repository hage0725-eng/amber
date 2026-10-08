"""閘門 A：ERP 彙總原檔健檢（班長產出後、DPR 分析前）。

用法：python flow/intake.py <原檔.xls/.xlsx> <狀態資料夾> [--now 2026-10-08T09:40] [--mtime 2026-10-08T09:12]
（從 Drive 下載的檔，--mtime 要給 Drive 的修改時間，換算成越南時間）
通過 → exit 0，並把本次筆數記入 <狀態資料夾>/intake_history.csv 當下次比較基準。
不通過 → exit 1，列出原因；不分析、不分派，等 Amber 或班長處理。
"""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import sys
from pathlib import Path

import pandas as pd

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "core"))
from paiho_core import load_rules, to_float  # noqa: E402


def _h(c) -> str:
    return " ".join(str(c).replace("\n", " ").split())


VN = dt.timezone(dt.timedelta(hours=7))     # 越南無日光節約，固定 +7，不依賴 tzdata


def vn_naive(t):
    """任何時間（含 Z / +00:00）→ 越南當地 naive 時間；naive 視為已是越南時間。"""
    if t is None:
        return None
    if isinstance(t, str):
        t = dt.datetime.fromisoformat(t.replace("Z", "+00:00"))
    return t.astimezone(VN).replace(tzinfo=None) if t.tzinfo else t


def find(cols, name):
    """表頭比對：去換行後以 name 開頭；'#'、'#2' 必須整格完全相等（避開 '# Nét'、'#.1'）。"""
    if name in ("#", "#2"):
        hits = [c for c in cols if _h(c) == name]
    else:
        hits = [c for c in cols if _h(c).startswith(name)]
    return hits[0] if hits else None


def _read(path, sheet, required):
    """讀原檔：支援 .xls / .xlsx / 實為 HTML 的 .XLS；表頭不在第 1 列時往下找（前 10 列）。"""
    head = Path(path).read_bytes()[:4096].lstrip().lower()
    if head.startswith((b"<html", b"<!doctype", b"<table")) or b"<table" in head:
        # 有些 ERP 匯出的 .XLS 其實是 HTML 表格；只有一張表，不檢查分頁名
        import io as _io
        data, text = Path(path).read_bytes(), None
        for enc in ("utf-8-sig", "utf-16", "cp950", "big5", "cp1258", "cp1252"):
            try:
                cand = data.decode(enc)
            except UnicodeDecodeError:
                continue
            if any(k in cand for k in ("訂單號碼", "客戶", "Mã đơn")):
                text = cand
                break
        if text is None:
            raise ValueError("HTML 原檔編碼無法辨識（試過 utf-8 / utf-16 / cp950 / big5 / cp1258）")
        t = pd.read_html(_io.StringIO(text))[0].astype(object)
        head_row = [c[-1] if isinstance(c, tuple) else c for c in t.columns]   # <thead> 會被吃成欄名，放回第 1 列
        raw = pd.concat([pd.DataFrame([head_row]), pd.DataFrame(t.values)], ignore_index=True)
    else:
        engine = "xlrd" if Path(path).suffix.lower() == ".xls" else None
        xl = pd.ExcelFile(path, engine=engine)
        if sheet not in xl.sheet_names:
            return None, f"找不到「{sheet}」，現有：{', '.join(xl.sheet_names)}"
        raw = pd.read_excel(xl, sheet_name=sheet, header=None, dtype=object)
    for r in range(min(10, len(raw))):
        cols = [_h(v) for v in raw.iloc[r].tolist()]
        if sum(1 for n in required if find(cols, n) is not None) >= len(required) * 0.6:
            df = raw.iloc[r + 1:].copy()
            df.columns = [str(v) for v in raw.iloc[r].tolist()]
            df = df.dropna(how="all")
            return df.reset_index(drop=True), f"表頭在第 {r + 1} 列"
    df = raw.iloc[1:].copy()
    df.columns = [str(v) for v in raw.iloc[0].tolist()]
    return df.reset_index(drop=True), "表頭找不到，暫以第 1 列判讀"


def check(path, state_dir, now=None, mtime=None, accept=False):
    C = load_rules()["flow"]["intake"]
    path, state_dir = Path(path), Path(state_dir)
    now = vn_naive(now) or vn_naive(dt.datetime.now(dt.timezone.utc))
    mtime = vn_naive(mtime)
    res = []          # (ok, 項目, 說明)

    # 從 Drive 下載時本機修改時間＝下載時間，須改傳 Drive 的 modifiedTime（--mtime）
    mt = mtime or dt.datetime.fromtimestamp(path.stat().st_mtime)
    age_h = (now - mt).total_seconds() / 3600
    res.append((0 <= age_h <= C["max_file_age_hours"], "檔案新鮮度",
                f"修改於 {age_h:.1f} 小時前（上限 {C['max_file_age_hours']}）"))

    try:
        df, note = _read(path, C["sheet"], C["required_columns"])
    except Exception as e:
        res.append((False, "開檔", f"無法開啟：{type(e).__name__}: {e}"[:200]))
        return _finish(res, path, state_dir, None, now)
    if df is None:
        res.append((False, "分頁", note))
        return _finish(res, path, state_dir, None, now)
    res.append((True, "分頁", f"「{C['sheet']}」{len(df)} 列 × {df.shape[1]} 欄（{note}）"))

    miss = [n for n in C["required_columns"] if find(df.columns, n) is None]
    res.append((not miss, "必要欄位", "齊全" if not miss else f"缺少：{'、'.join(miss)}"))
    if miss:
        return _finish(res, path, state_dir, len(df), now)

    oc = find(df.columns, "訂單號碼")
    blank = df[oc].isna() | df[oc].astype(str).str.strip().isin(["", "nan", "None"])
    br = blank.mean()
    res.append((br <= C["max_blank_order_ratio"], "空白訂單號",
                f"{blank.sum()} 列（{br:.2%}，上限 {C['max_blank_order_ratio']:.0%}；R-0820-2 會剔除）"))

    body = df[~blank]
    keys = [find(df.columns, k) for k in C["dedup_key"]]
    miss_k = [k for k, c in zip(C["dedup_key"], keys) if c is None]
    if miss_k:
        res.append((False, "去重鍵欄位", f"缺少：{'、'.join(miss_k)}"))
        return _finish(res, path, state_dir, len(df), now)
    dup = body.duplicated(subset=keys).sum()
    dr = dup / max(len(body), 1)
    res.append((dr <= C["max_dup_ratio"], "重複鍵", f"{dup} 列（{dr:.2%}，上限 {C['max_dup_ratio']:.0%}）"))

    done = body[find(df.columns, "已完成訂單")].astype(str).str.contains("✔", na=False)
    active = int((~done).sum())
    res.append((active > 0, "未完成訂單", f"{active} 筆"))

    pdcol = find(df.columns, "生產天數")
    act = body[~done]
    num = act[pdcol].map(lambda v: to_float(v) is not None).mean() if len(act) else 0
    res.append((num >= C["min_numeric_prod_days"], "生產天數可讀",
                f"{num:.1%}（下限 {C['min_numeric_prod_days']:.0%}）"))

    last = _last_pass(state_dir)
    sha = _sha(path)
    if last and last["sha"] == sha and last["date"][:10] == now.isoformat()[:10]:
        res.append((True, "重跑", f"與今天 {last['date'][11:16]} 通過的是同一份檔，視為重跑"))
    elif last:
        chg = abs(len(df) - last["rows"]) / max(last["rows"], 1)
        ok_chg = chg <= C["max_row_change_ratio"] or accept
        res.append((ok_chg, "筆數變動",
                    f"{last['rows']} → {len(df)}（{chg:.1%}，上限 {C['max_row_change_ratio']:.0%}；比對 {last['date']}）"
                    + ("｜Amber 已確認接受（--accept）" if accept and chg > C["max_row_change_ratio"] else "")))
        res.append((last["sha"] != sha, "與上次不同檔",
                    "內容與前一次通過的完全相同＝班長可能沒重新匯出" if last["sha"] == sha else "內容已更新"))
    else:
        res.append((True, "筆數變動", "首次執行，無基準（本次通過後建立）"))
    return _finish(res, path, state_dir, len(df), now, rerun=bool(last and last["sha"] == sha
                   and last["date"][:10] == now.isoformat()[:10]))


def _sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]


def _last_pass(state_dir):
    f = Path(state_dir) / "intake_history.csv"
    if not f.exists():
        return None
    rows = [r for r in csv.DictReader(open(f, encoding="utf-8")) if r["result"] == "PASS"]
    if not rows:
        return None
    r = rows[-1]
    return {"rows": int(r["rows"]), "date": r["time"][:16], "sha": r["sha"]}


def _finish(res, path, state_dir, rows, now, rerun=False):
    ok = all(r[0] for r in res)
    print("=" * 56)
    print(f"閘門 A 原檔健檢｜{path.name}")
    for good, item, note in res:
        print(f"{'✅' if good else '❌'} {item}：{note}")
    print("==> 通過，可進入分析" if ok else "==> 停線：不分析、不分派，請班長重新匯出或通知 Amber")
    state_dir = Path(state_dir)
    state_dir.mkdir(parents=True, exist_ok=True)
    f = state_dir / "intake_history.csv"
    new = not f.exists()
    with open(f, "a", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        if new:
            w.writerow(["time", "file", "rows", "sha", "result", "fails"])
        if not rerun:                          # 重跑不另記一筆，避免基準被洗掉
            w.writerow([now.isoformat(timespec="minutes"), path.name, rows or 0, _sha(path),
                        "PASS" if ok else "FAIL", "；".join(i for g, i, _ in res if not g)])
    return ok, res


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("file")
    ap.add_argument("state_dir")
    ap.add_argument("--now", help="執行時間，可帶時區（如 2026-10-08T02:45Z）")
    ap.add_argument("--mtime", help="Drive 修改時間，可帶時區（如 2026-10-08T02:12:00Z）")
    ap.add_argument("--accept", action="store_true", help="Amber 已確認筆數大幅變動屬實，接受本次")
    x = ap.parse_args()
    ok, _ = check(x.file, x.state_dir, x.now, x.mtime, x.accept)
    sys.exit(0 if ok else 1)
