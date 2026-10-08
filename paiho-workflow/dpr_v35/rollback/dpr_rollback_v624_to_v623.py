# -*- coding: utf-8 -*-
"""dpr_rollback_v624_to_v623.py — 由 dpr_suite.py v624 逐位元組重建 v623（R-1002-27 備份·R-1002-26 同法）
用法：python3 dpr_rollback_v624_to_v623.py <v624 dpr_suite.py> <輸出 v623 路徑>（自足：EDITS 內嵌）
輸出 SHA256 必須＝f18f4640…；再往前：dpr_rollback_v623_to_v622.py → dpr_rollback_v622_to_v621.py。
"""
import hashlib, importlib.util, os, shutil, sys, tempfile
V624_SHA = 'c02ed0281be360a85f09d166347ca7c0672e3d554f6c30e9b3508b7e5366ff5f'
V623_SHA = 'f18f464021d92e654082342395e6bb8ab70cc010c326842f8da882a804a4285f'
EDITS = [
    ('# FILE_VERSION = 595   # R-v555-1（Amber 0730「轉正」）：降版閘門用·改本檔須同步遞增\n',
     '# FILE_VERSION = 596   # R-v555-1（Amber 0730「轉正」）：降版閘門用·改本檔須同步遞增\n'
     '#   v596（2026-10-02·**R-1002-27**·Amber 林彥博 P-1001-T9「按照C」＋F／T 例外、0／Q 算完成、落 B3、aging 看回復客戶日）：\n'
     '#        保留足（AN✔＋保留量依單位換算≥數量＋完工0未交）→ 主分析 OK、轉 B3「📦保留足待出貨」；測試 F／T → 不視為完成、B3「🧪測試例外」。\n'
     '#        A1 不收保留足完成列；R-0922-7／8 斷言豁免之。其他判定式、OTD、分頁一行未動。\n'),
    # ① 判定前計算 rsv
    ("    bl_ok = dnz(r[39]) == '✔'\n",
     "    bl_ok = dnz(r[39]) == '✔'\n"
     "    # ══ R-1002-27 保留足判定（Amber 林彥博 2026-10-02 P-1001-T9「按照C」）══\n"
     "    _rq, _rbq = fnum(r[15]), fnum(r[23])\n"
     "    _ru, _rbu = dnz(r[16]), dnz(r[24]).upper()\n"
     "    _rconv = (_rbq * 0.9144 if (_rbu == '1Y' and _ru == '米') else\n"
     "              (_rbq if RSV_UNIT.get(_rbu) == _ru else None))\n"
     "    rsv = ((not is89) and bl_ok and _rq > 0 and _rconv is not None and _rconv >= _rq - 1e-6\n"
     "           and fnum(r[20]) < _rq and fnum(r[21]) < _rq)\n"),
    # 常數
    ("HIGH = '🔴 高風險 / Rủi ro cao HIGH'\n",
     "HIGH = '🔴 高風險 / Rủi ro cao HIGH'\n"
     "RSV_UNIT = {'1Y': '碼', '9D': '雙', '9P': 'PC', '6K': 'KG'}   # R-1001-21／R-0924-19 單位碼（R-1002-27 保留足換算用）\n"
     "RSV_EXC_TESTS = ('F', 'T')                                   # R-1002-27：保留足但測試 F／T 不視為完成\n"
     "RSV_NOTE = {'Q': '特採出貨 / Đặc chuẩn', '0': '報告未到 / Chưa có BC KT', 'B': '測試後補 / Bổ sung KT sau'}\n"),
    # ③ 例外原因取代「保留需確認」
    ("            if bl_ok:\n                reasons.append('⚠️保留需確認是否成品 / Cần XN tồn kho TP')\n",
     "            if bl_ok and rsv and test in RSV_EXC_TESTS:   # R-1002-27 ③\n"
     "                reasons.append('🧪保留足但測試%s·不視為完成·例外追蹤重測或特採 / Bảo lưu đủ nhưng KT %s, theo dõi ngoại lệ' % (test, test))\n"
     "            elif bl_ok:\n                reasons.append('⚠️保留需確認是否成品 / Cần XN tồn kho TP')\n"),
    # ② 改判 OK（在 risk 計算之前）
    ("    if is89:\n        risk = '— / DB 89'\n",
     "    rsv_state = None\n"
     "    if rsv and test in RSV_EXC_TESTS:\n"
     "        rsv_state = 'exc'\n"
     "    elif rsv and not (prio or major):   # R-1002-27 ②：保留足視同完成（⭐／🆘 照舊不降）\n"
     "        rsv_state = 'done'\n"
     "        level = 'OK'\n"
     "        reasons = ['📦保留足·視同完成·轉 B3 待出貨（R-1002-27） / Bảo lưu đủ, coi như hoàn thành, theo dõi giao ở B3']\n"
     "        if test in RSV_NOTE:\n"
     "            reasons.append(RSV_NOTE[test])\n"
     "    if is89:\n        risk = '— / DB 89'\n"),
    # 處置
    ("        if '保留需確認' in rtxt:\n",
     "        if '保留足·視同完成' in rtxt:   # R-1002-27\n"
     "            disp.append('業務／倉庫安排出貨，已過回復客戶日先回客戶出貨日（B3 追蹤） / NV & kho sắp xếp giao, quá hẹn thì báo KH ngày giao')\n"
     "        if '🧪保留足但測試' in rtxt:   # R-1002-27\n"
     "            disp.append('品保／工程追重測結果或特採核准進度 / QA theo dõi KQ test lại hoặc tiến độ đặc chuẩn')\n"
     "        if '保留需確認' in rtxt:\n"),
    ("                'bc': bc, 'bn': bn, 'pm': pm, 'prio': prio, 'major': major,\n",
     "                'bc': bc, 'bn': bn, 'pm': pm, 'prio': prio, 'major': major, 'rsv': rsv_state, 'test': test,\n"),
    # ⑤ A1 不收 done
    ("    if a['is89'] or not a.get('okh'):\n        continue\n    r = a['row']\n    _sq = as_date(r[7]) or as_date(r[6])\n",
     "    if a['is89'] or not a.get('okh') or a.get('rsv') == 'done':   # R-1002-27：保留足完成列改由 B3 追蹤\n        continue\n    r = a['row']\n    _sq = as_date(r[7]) or as_date(r[6])\n"),
    # ④ B3 收保留足兩類
    ("B3_ROWS.sort(key=lambda x: (0 if x[0].startswith('⚠️') else 1, -x[12], x[3]))\n"
     "assert not any((x[4], x[5], x[7], x[15]) in _ana_keys for x in B3_ROWS), 'R-0922-13 違例：B3 列不得出現在主分析'\n"
     "assert all(x[9] >= x[8] > x[10] for x in B3_ROWS), 'R-0922-13 違例：B3 只收完工足數且未交足之列'\n",
     "_B3_DONE_N = len(B3_ROWS)\n"
     "assert not any((x[4], x[5], x[7], x[15]) in _ana_keys for x in B3_ROWS), 'R-0922-13 違例：B3 完工足數列不得出現在主分析'\n"
     "assert all(x[9] >= x[8] > x[10] for x in B3_ROWS), 'R-0922-13 違例：B3 只收完工足數且未交足之列'\n"
     "# ══ R-1002-27（Amber 林彥博 2026-10-02）B3 加收保留足兩類：📦待出貨（視同完成）／🧪測試 F／T 例外 ══\n"
     "for a in ANA:\n"
     "    if a['is89'] or a.get('rsv') not in ('done', 'exc'):\n"
     "        continue\n"
     "    r = a['row']\n"
     "    _kh = as_date(r[5]); _od = ((TODAY - _kh).days if _kh and _kh < TODAY else 0)\n"
     "    if a['rsv'] == 'exc':\n"
     "        st = '🧪測試%s例外·保留足但不可出貨·追重測／特採 / Ngoại lệ KT %s, chưa được giao' % (a['test'], a['test'])\n"
     "    else:\n"
     "        _nt = RSV_NOTE.get(a['test'], '').split(' / ')[0]\n"
     "        st = (('📦保留足·已過回復客戶日·未交 / Bảo lưu đủ, quá hẹn KH' if _od > 0 else\n"
     "               ('📦保留足·回復客戶日未到·待交 / Bảo lưu đủ, chưa đến hạn' if _kh else '📦保留足·回復客戶空白 / Bảo lưu đủ, chưa có ngày TL KH'))\n"
     "              + ('（%s）' % _nt if _nt else ''))\n"
     "    B3_ROWS.append([st, a['tl'], a['code'], a['sc'] or a['code'], a['order'], dnz(r[3]), dnz(r[0]),\n"
     "                    dnz(r[11]), fnum(r[15]), fnum(r[20]), fnum(r[21]), dstr(r[5]), _od, dnz(r[18]), '', dnz(r[12]),\n"
     "                    *b3_prev(r[2], r[3], _od)])\n"
     "_b3k = lambda x: (0 if '已過回復客戶日' in x[0] else (1 if x[0].startswith('🧪') else 2), -x[12], x[3])\n"
     "B3_ROWS.sort(key=_b3k)\n"
     "assert all(a['level'] == 'OK' for a in ANA if a.get('rsv') == 'done'), 'R-1002-27 違例：保留足完成列未改 OK'\n"
     "assert not any(a.get('rsv') == 'done' and a['test'] in RSV_EXC_TESTS for a in ANA), 'R-1002-27 違例：測試 F／T 不得視為完成'\n"
     "assert len(B3_ROWS) == _B3_DONE_N + sum(1 for a in ANA if a.get('rsv') in ('done', 'exc')), 'R-1002-27 違例：B3 保留足列數不符'\n"),
    ("put(wsB3, _rB, 1, '★ R-0922-13：本頁只列「已完工足數但未交足」的單，",
     "put(wsB3, _rB, 1, '★ R-1002-27：另收「📦保留足待出貨」（保留量足、視同完成、主分析記 OK）與「🧪測試 F／T 例外」（保留足但不可出貨，追重測或特採）兩類，完工量欄為 0 屬正常。 / Thêm 2 loại: 📦 bảo lưu đủ chờ giao (coi như HT) và 🧪 ngoại lệ KT F/T. '\n"
     "                  '★ R-0922-13：完工足數列＝「已完工足數但未交足」的單，"),
    ("f\"R-0922-10 A1 {len(A1_ROWS)} 列｜R-0922-13 B3 {len(B3_ROWS)} 列（已過回復客戶日 {sum(1 for x in B3_ROWS if x[0].startswith('⚠️'))}）\")",
     "f\"R-0922-10 A1 {len(A1_ROWS)} 列｜R-0922-13 B3 {len(B3_ROWS)} 列（完工足數 {_B3_DONE_N}·已過回復客戶日 {sum(1 for x in B3_ROWS if '已過回復客戶日' in x[0])}｜R-1002-27 📦 {sum(1 for x in B3_ROWS if x[0].startswith('📦'))}／🧪 {sum(1 for x in B3_ROWS if x[0].startswith('🧪'))}）\")"),
    # R-0922-7/8 斷言豁免
    ("assert all(a['level'] in ('WARNING', 'DELAY') for a in ANA if not a['is89'] and (a.get('b1') or a.get('b2'))\n",
     "assert all(a['level'] in ('WARNING', 'DELAY') for a in ANA if not a['is89'] and (a.get('b1') or a.get('b2')) and a.get('rsv') != 'done'\n"),
]

SUITE_DOC_OLD = '"""dpr_suite.py — DPR 迴歸/迴路單檔套件（v623·1002 7w 白名單 v1.10）\n'
SUITE_DOC_NEW = ('"""dpr_suite.py — DPR 迴歸/迴路單檔套件（v624·1002 保留足視同完成）\n'
                 'v624（2026-10-02·**R-1002-27**·Amber 林彥博 P-1001-T9「按照C」＋F／T 例外、0／Q 算完成、落 B3、aging 看回復客戶日）：\n'
                 '  · _PACK 只換 build_dpr.py（FILE_VERSION 595→596）：保留足（AN✔＋保留量換算≥數量＋完工0未交）→ 主分析 OK、B3「📦保留足待出貨」；\n'
                 '    測試 F／T → 不視為完成、B3「🧪測試例外」；A1 不收保留足完成列。棒次、快照 v574、字典 v95、overrides v1.10 一行未動。SUITE_VERSION 623 → 624。\n'
                 'v623（2026-10-02·**R-1001-23／R-1002-19**·Amber 林彥博「B4-ok」「B14-OK」；v622 上線後照硬序上·R-1002-25）：\n')
SUITE_DOC_OLD2 = 'v623（2026-10-02·**R-1001-23／R-1002-19**·Amber 林彥博「B4-ok」「B14-OK」；v622 上線後照硬序上·R-1002-25）：\n'



def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m); return m
def main(src, dst):
    assert sha(src) == V624_SHA, 'v624 雜湊不符：%s' % sha(src)
    work = tempfile.mkdtemp(prefix='rb623_'); suite = os.path.join(work, 'dpr_suite.py'); shutil.copy(src, suite)
    m = load(suite, 's624'); pk = os.path.join(work, 'pack'); m.restore(pk, force=True)
    bp = os.path.join(pk, 'build_dpr.py'); s = open(bp, encoding='utf-8').read()
    for old, new in reversed(EDITS):
        assert s.count(new) == 1, '反向點命中 %d 次：%r' % (s.count(new), new[:60]); s = s.replace(new, old)
    open(bp, 'w', encoding='utf-8').write(s); m.pack(pk)
    t = open(suite, encoding='utf-8').read()
    assert t.count('SUITE_VERSION = 624') == 1 and t.count(SUITE_DOC_NEW) == 1
    t = t.replace('SUITE_VERSION = 624', 'SUITE_VERSION = 623').replace(SUITE_DOC_NEW, SUITE_DOC_OLD + SUITE_DOC_OLD2)
    open(dst, 'w', encoding='utf-8').write(t); shutil.rmtree(work)
    assert sha(dst) == V623_SHA, '重建 v623 雜湊不符：%s' % sha(dst)
    print('v623 重建 OK  SHA256=%s  bytes=%d' % (sha(dst), os.path.getsize(dst)))
if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
