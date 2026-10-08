"""給 Amber 的每日摘要（Markdown），照她的回報格式：第一句結論、1. 2. 3.、==>、決策以問句結尾。

用法：python flow/digest.py <狀態資料夾> [回填狀態.xlsx] > 摘要.md
"""
from __future__ import annotations

import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path

import openpyxl

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def _last_intake(state_dir):
    f = Path(state_dir) / "intake_history.csv"
    if not f.exists():
        return None
    rows = list(csv.DictReader(open(f, encoding="utf-8")))
    return rows[-1] if rows else None


def _md(ts: str) -> str:
    """ISO 時間 → M/D HH:MM（Amber 偏好的短日期）。"""
    try:
        import datetime as dt
        d = dt.datetime.fromisoformat(ts)
        return f"{d.month}/{d.day} {d:%H:%M}"
    except Exception:
        return ts


def _rows(ws):
    it = ws.iter_rows(values_only=True)
    head = next(it, None)
    return [r for r in it if any(v is not None for v in r)] if head else []


def build(state_dir, status_xlsx=None, max_list=15):
    out = []
    intake = _last_intake(state_dir)
    st, pend, issues = Counter(), [], []
    if status_xlsx and Path(status_xlsx).exists():
        wb = openpyxl.load_workbook(status_xlsx, data_only=True)
        for r in _rows(wb.worksheets[1]):
            st[r[3]] += 1
            pend.append(r)
        for r in _rows(wb.worksheets[0]):
            st["已回填"] += r[1] or 0
        issues = _rows(wb.worksheets[2])

    total = sum(st.values())
    if intake and intake["result"] != "PASS":
        head = f"今天原檔沒過閘門 A（{intake['fails']}），已停線，沒有分析也沒有分派。"
    elif total:
        rate = st["已回填"] / total
        head = f"回填完成率 {rate:.0%}（{st['已回填']}/{total}），需妳處理 {len(issues)} 件、待追 {total - st['已回填']} 列。"
    else:
        head = "原檔已通過閘門 A，等待分析與分派。"
    out.append(head)
    out.append("")

    out.append("1. 自動完成")
    if intake:
        out.append(f"   原檔 {intake['file']}｜{intake['rows']} 列｜閘門 A {'通過' if intake['result'] == 'PASS' else '停線'}（{_md(intake['time'])}）")
    if total:
        out.append(f"   ==> 已回填 {st['已回填']} 列，已寫回分析檔原位，其他儲存格逐格驗證未變動")

    out.append("")
    out.append("2. 需要妳處理")
    if intake and intake["result"] != "PASS":
        out.append(f"   原檔停線：{intake['fails']}｜{_md(intake['time'])}｜班長｜ERP 匯出")
    if issues:
        for i in issues[:max_list]:
            who = i[4] if len(i) > 4 and i[4] else ""
            order = i[5] if len(i) > 5 and i[5] else i[1]
            out.append(f"   {order}｜{who}｜{i[0]}（{i[3]}）｜回填步驟")
        if len(issues) > max_list:
            out.append(f"   …另 {len(issues) - max_list} 件見回填狀態表")
    if not (issues or (intake and intake["result"] != "PASS")):
        out.append("   ==> 無")

    out.append("")
    out.append("3. 待追（依助理）")
    by = defaultdict(Counter)
    for owner, _sheet, _row, s, _ref in pend:
        by[owner][s] += 1
    if not by:
        out.append("   ==> 無")
    for owner, c in sorted(by.items(), key=lambda x: -sum(x[1].values())):
        out.append(f"   {owner}：" + "、".join(f"{k} {v}" for k, v in c.most_common()))
    return "\n".join(out)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    print(build(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None))
