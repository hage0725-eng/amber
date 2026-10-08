"""回填攻擊測試：獨立審查找到的實際出錯方式，每一種都要被擋下或正確處理。"""
from __future__ import annotations

import contextlib
import io
import os
import shutil
import sys
import tempfile
import time
import unicodedata
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "flow"))
import backfill as bf  # noqa: E402

FIXTURE = ROOT / "tests" / "fixtures" / "T組進度完整分析_0916.xlsx"


def _quiet(fn, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*a, **k)


def _first_rows(path, n=3):
    """回傳該檔第一張資料分頁的 (ws 名, 前 n 列列號, 表頭)。"""
    wb = openpyxl.load_workbook(path)
    ws = wb.worksheets[1]
    hdr = [bf.norm(c.value) for c in ws[1]]
    return ws.title, list(range(2, min(ws.max_row, n + 1) + 1)), hdr


def _fill(path, edits, dst=None):
    wb = openpyxl.load_workbook(path)
    ws = wb.worksheets[1]
    hdr = [bf.norm(c.value) for c in ws[1]]
    ki = hdr.index(bf.KEY_COL)
    req = bf.required_idx(hdr[:ki], bf.cfg())
    keys = {}
    for r, v in edits.items():
        ws.cell(r, req[0] + 1).value = v
        if isinstance(v, str) and v.startswith("="):
            ws.cell(r, req[0] + 1).data_type = "s"     # 模擬使用者以文字輸入（Excel 前置 '）
        keys[r] = ws.cell(r, ki + 1).value
    wb.save(dst or path)
    return keys, req[0]


def _master_val(merged, key, col):
    _t, title, r = key.split("|")
    return openpyxl.load_workbook(merged)[title].cell(int(r), col + 1)


def run():
    tmp = Path(tempfile.mkdtemp(prefix="bf_atk_"))
    fails = []
    try:
        out = tmp / "split"
        _quiet(bf.split, FIXTURE, out)
        target = sorted(out.glob("*.xlsx"), key=lambda p: -p.stat().st_size)[0]   # 最大的一份

        # A 舊日期檔＋同日重複檔：0915 不寫回；同日兩份取較新
        back = tmp / "A"
        back.mkdir()
        old = back / target.name.replace("_0916_", "_0915_")
        wb = openpyxl.load_workbook(target)
        for ws in wb.worksheets[1:]:
            hdr = [bf.norm(c.value) for c in ws[1]]
            ki = hdr.index(bf.KEY_COL)
            for r in range(2, ws.max_row + 1):
                ws.cell(r, ki + 1).value = str(ws.cell(r, ki + 1).value).replace("0916|", "0915|", 1)
        wb.save(old)
        _fill(old, {2: "YESTERDAY"})
        dup_old = back / target.name.replace(".xlsx", " (1).xlsx")
        keys, ci = _fill(target, {2: "OLDER COPY"}, dup_old)
        time.sleep(1.1)
        _fill(target, {2: "NEWEST"}, back / target.name)
        os.utime(dup_old, (time.time() - 3600, time.time() - 3600))
        cnt, issues, merged = _quiet(bf.collect, FIXTURE, back, tmp / "A_res")
        v = bf.norm(_master_val(merged, keys[2], ci).value)
        if v != "NEWEST":
            fails.append(f"A 舊日期/重複檔：寫回「{v}」")
        if not any(i[0] == "日期不符" for i in issues):
            fails.append("A 0915 檔沒被標日期不符")

        # B 「=」開頭文字不可變公式；日期輸入存成文字
        back = tmp / "B"
        back.mkdir()
        keys, ci = _fill(target, {2: "==> đã xử lý", 3: "=SUM(1,2)"}, back / target.name)
        _cnt, _iss, merged = _quiet(bf.collect, FIXTURE, back, tmp / "B_res")
        for r, want in ((2, "==> đã xử lý"), (3, "=SUM(1,2)")):
            c = _master_val(merged, keys[r], ci)
            if c.data_type == "f" or bf.norm(c.value) != want:
                fails.append(f"B 「{want}」變成公式或值不符")

        # C 組員清空 → 寫回空白；Amber 拆檔後改過的格，組員再改＝衝突，保留 Amber
        m2 = tmp / "C_master" / FIXTURE.name
        m2.parent.mkdir()
        shutil.copy(FIXTURE, m2)
        mk = openpyxl.load_workbook(target).worksheets[1]
        hdr = [bf.norm(c.value) for c in mk[1]]
        ki = hdr.index(bf.KEY_COL)
        k3 = mk.cell(3, ki + 1).value
        _t, title, r3 = k3.split("|")
        mw = openpyxl.load_workbook(m2)
        req = bf.required_idx(hdr[:ki], bf.cfg())[0]
        mw[title].cell(int(r3), req + 1).value = "AMBER EDIT"
        mw.save(m2)
        back = tmp / "C"
        back.mkdir()
        keys, ci = _fill(target, {3: "ASSISTANT EDIT"}, back / target.name)
        _cnt, issues, merged = _quiet(bf.collect, m2, back, tmp / "C_res")
        if bf.norm(_master_val(merged, keys[3], ci).value) != "AMBER EDIT":
            fails.append("C 衝突時沒保留 Amber 版本")
        if not any(i[0] == "與 Amber 修改衝突" for i in issues):
            fails.append("C 衝突沒列入異常")

        # C2 組員清空：拆檔時已有內容的格，組員刪掉 → 彙總也要變空白
        m3 = tmp / "C2_master" / FIXTURE.name
        m3.parent.mkdir()
        mw = openpyxl.load_workbook(FIXTURE)
        mw[title].cell(int(r3), req + 1).value = "PREFILLED"
        mw.save(m3)
        out3 = tmp / "C2_split"
        _quiet(bf.split, m3, out3)
        back = tmp / "C2"
        back.mkdir()
        cleared = False
        for f in out3.glob("*.xlsx"):
            wb = openpyxl.load_workbook(f)
            for ws in wb.worksheets[1:]:
                h = [bf.norm(c.value) for c in ws[1]]
                kk = h.index(bf.KEY_COL)
                for rr in range(2, ws.max_row + 1):
                    if ws.cell(rr, kk + 1).value == k3:
                        ws.cell(rr, req + 1).value = None
                        cleared = True
            wb.save(back / f.name)
        _cnt, _iss, merged = _quiet(bf.collect, m3, back, tmp / "C2_res")
        if not cleared or bf.norm(_master_val(merged, k3, req).value) != "":
            fails.append("C2 組員清空沒有寫回")

        # D .xls / 其他格式交回 → 列為異常，不默默略過
        back = tmp / "D"
        back.mkdir()
        (back / "DPR_0916_X.xls").write_bytes(b"not really xls")
        (back / "DPR_0916_Y.gsheet").write_text("{}")
        _cnt, issues, _m = _quiet(bf.collect, FIXTURE, back, tmp / "D_res")
        if sum(1 for i in issues if i[0] == "無法讀取的檔案") != 2:
            fails.append("D 非 xlsx 交回沒全部列為異常")

        # E 寫錯列的 bug 必須被合併驗證抓到（注入錯誤）
        back = tmp / "E"
        back.mkdir()
        _fill(target, {2: "ROW SHIFT"}, back / target.name)
        orig_save = openpyxl.Workbook.save

        def shifted_save(self, filename):
            for ws in self.worksheets:
                for row in ws.iter_rows():
                    for c in row:
                        if c.value == "ROW SHIFT":
                            ws.cell(c.row + 1, c.column).value, c.value = "ROW SHIFT", None
                            return orig_save(self, filename)
            return orig_save(self, filename)

        openpyxl.Workbook.save = shifted_save
        try:
            _quiet(bf.collect, FIXTURE, back, tmp / "E_res")
            fails.append("E 寫錯列沒被抓到")
        except SystemExit:
            if any((tmp / "E_res").glob("*_回填彙總.xlsx")):
                fails.append("E 驗證失敗仍留下彙總檔")
        finally:
            openpyxl.Workbook.save = orig_save

        # F 名字：NFC/NFD 同一人；錯誤值不當人名；不同人撞檔名加序號
        C = bf.cfg()
        hdr = ["助理 / Trợ lý"]
        n1 = bf.owner_of([unicodedata.normalize("NFD", "Dương Thị Yến Nhi")], hdr, C)
        n2 = bf.owner_of([unicodedata.normalize("NFC", "Dương Thị Yến Nhi")], hdr, C)
        if n1 != n2:
            fails.append("F NFC/NFD 被當成兩個人")
        for bad in ("#REF!", "0", "#N/A", ""):
            if bf.owner_of([bad], hdr, C) != C["unassigned"]:
                fails.append(f"F 「{bad}」被當成人名")
        if bf.slug("Nguyễn Thị Hà") != bf.slug("Nguyễn Thị Hạ"):
            fails.append("F 撞名測試前提不成立")      # 兩個不同人轉成同一檔名，split 會加 -2

        if fails:
            return False, "；".join(fails)
        return True, "8 類實際出錯方式（舊檔/重複檔/公式/清空/衝突/異格式/寫錯列/人名）全部擋下"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    ok, msg = run()
    print(("✅ " if ok else "❌ ") + msg)
    sys.exit(0 if ok else 1)
