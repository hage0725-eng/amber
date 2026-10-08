# -*- coding: utf-8 -*-
"""dpr_rollback_v622_to_v621.py — 由 dpr_suite.py v622 逐位元組重建 v621（R-1002-25 E6 備份閘）
用法：python3 dpr_rollback_v622_to_v621.py <v622 dpr_suite.py> <輸出 v621 路徑>（自足：EDITS 已內嵌，不需補丁檔）
原理：v622 只比 v621 多 8 處 build_dpr.py 字串替換＋SUITE_VERSION＋docstring 4 行；把補丁的 EDITS 反向套回、重打包，
      輸出 SHA256 必須＝d3b94b5c74e1c51e250cbca653735d91562179fc7b9b8d86df7a0df33d20f5b2，否則中止。
"""
import hashlib, importlib.util, os, shutil, sys, tempfile
V622_SHA = '41138cd04c7f5b2a91ed5c93fcdc531e85ad4e655e99dd71d6f537e463b2aeb8'
V621_SHA = 'd3b94b5c74e1c51e250cbca653735d91562179fc7b9b8d86df7a0df33d20f5b2'
EDITS = [
    ('# FILE_VERSION = 594   # R-v555-1（Amber 0730「轉正」）：降版閘門用·改本檔須同步遞增\n',
     '# FILE_VERSION = 595   # R-v555-1（Amber 0730「轉正」）：降版閘門用·改本檔須同步遞增\n'
     '#   v595（2026-10-01·**R-1001-16**·Amber 林彥博「A3 直接修改改讀 AO 欄」「89 也看 AO」）：\n'
     '#        完成判定改讀 AO「入庫夠數量」（DONE_COL=40，依 R-0930-21），AP「已完成訂單」不再讀；89 列同。\n'
     '#        範本刪除 AP 欄時於 col41 補空白虛擬欄，TL／業務欄位置不變。主分析異常判定式一行未動。\n'),
    ('NCOLS = len(COLMAP)\nassert NCOLS in (44, 45)',
     '# ══ R-1001-16（Amber 林彥博 2026-10-01）AP 欄刪除容錯：依檔名前綴之契約欄數判定 ══\n'
     '_INB0 = INPUT.split(\'/\')[-1]\n'
     '_EXPECT = 44 if re.match(r\'^T1[組\\s_\\-]\', _INB0) else (45 if re.match(r\'^T[組\\s_\\-]\', _INB0) else None)\n'
     'AP_ABSENT = (_EXPECT is not None and len(COLMAP) == _EXPECT - 1)\n'
     'if AP_ABSENT:\n'
     '    COLMAP = COLMAP[:41] + [None] + COLMAP[41:]\n'
     '    print(\'  ℹ️ R-1001-16：追蹤表已無 AP「已完成訂單」欄 → col41 補空白虛擬欄（完成判定改讀 AO，不受影響）\')\n'
     'DONE_COL = 40   # R-1001-16／R-0930-21：完成判定＝AO「入庫夠數量」✔（89 列同）\n'
     'NCOLS = len(COLMAP)\nassert NCOLS in (44, 45)'),
    ("HDR = [dnz(sh.cell_value(0, c)) for c in COLMAP]",
     "HDR = [('' if c is None else dnz(sh.cell_value(0, c))) for c in COLMAP]"),
    ("    rows_raw.append([sh.cell_value(r, c) for c in COLMAP])",
     "    rows_raw.append([('' if c is None else sh.cell_value(r, c)) for c in COLMAP])"),
    ("def _tick_short(r):   # R-0922-12\n    return dnz(r[41]) == '✔'",
     "def _tick_short(r):   # R-0922-12（R-1001-16：改讀 AO）\n    return dnz(r[DONE_COL]) == '✔'"),
    ("active = [r for r in rows if dnz(r[41]) != '✔' or _tick_short(r)]",
     "active = [r for r in rows if dnz(r[DONE_COL]) != '✔' or _tick_short(r)]   # R-1001-16：AO 未✔ 才在途"),
    ("    if dnz(r[41]) != '✔' or dnz(r[0]) == '89' or not dnz(r[2]):",
     "    if dnz(r[DONE_COL]) != '✔' or dnz(r[0]) == '89' or not dnz(r[2]):   # R-1001-16：AO✔"),
    ("# 定義：已完成訂單✔（入庫夠數量）但 已交＜數量 之非 89 列。",
     "# 定義：AO 入庫夠數量✔（R-1001-16，原讀 AP 已完成訂單）但 已交＜數量 之非 89 列。"),
]

SUITE_DOC_OLD = '"""dpr_suite.py — DPR 迴歸/迴路單檔套件（v621·1001 DPR 瘦身輪）\n'
SUITE_DOC_NEW = ('"""dpr_suite.py — DPR 迴歸/迴路單檔套件（v622·1001 完成判定改讀 AO）\n'
                 'v622（2026-10-01·**R-1001-16**·Amber 林彥博「A3 直接修改改讀 AO 欄」「89 也看 AO」「先驗 v621 再上 v622」）：\n'
                 '  · _PACK 只換 build_dpr.py（FILE_VERSION 594→595）：完成判定 r[41]（AP）→ DONE_COL=40（AO），89 列同；\n'
                 '    AP 欄被刪時 col41 補空白虛擬欄。其餘 9 檔、棒次、快照 v574、字典 v95、判定式一行未動。SUITE_VERSION 621 → 622。\n')


def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m); return m
def main(src, dst):
    assert sha(src) == V622_SHA, 'v622 雜湊不符：%s' % sha(src)
    work = tempfile.mkdtemp(prefix='rb621_'); suite = os.path.join(work, 'dpr_suite.py'); shutil.copy(src, suite)
    m = load(suite, 's622'); pk = os.path.join(work, 'pack'); m.restore(pk, force=True)
    bp = os.path.join(pk, 'build_dpr.py'); s = open(bp, encoding='utf-8').read()
    for old, new in reversed(EDITS):
        assert s.count(new) == 1, '反向點命中 %d 次：%r' % (s.count(new), new[:60]); s = s.replace(new, old)
    open(bp, 'w', encoding='utf-8').write(s); m.pack(pk)
    t = open(suite, encoding='utf-8').read()
    assert t.count('SUITE_VERSION = 622') == 1 and t.count(SUITE_DOC_NEW) == 1
    t = t.replace('SUITE_VERSION = 622', 'SUITE_VERSION = 621').replace(SUITE_DOC_NEW, SUITE_DOC_OLD)
    open(dst, 'w', encoding='utf-8').write(t); shutil.rmtree(work)
    assert sha(dst) == V621_SHA, '重建 v621 雜湊不符：%s' % sha(dst)
    print('v621 重建 OK  SHA256=%s  bytes=%d' % (sha(dst), os.path.getsize(dst)))
if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
