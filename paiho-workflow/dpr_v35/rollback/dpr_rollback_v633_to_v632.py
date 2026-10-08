# -*- coding: utf-8 -*-
"""dpr_rollback_v633_to_v632.py — R-1002-26 回滾程式（R-1003-3 上線前備份閘）
用法：python3 dpr_rollback_v633_to_v632.py <v633 dpr_suite.py> <輸出 v632 路徑>
印出 SHA256 0a090270… ✅ 即為 v632 原檔。還原：docstring v633 段、SUITE_VERSION、_PACK['build_dpr.py']（反向套 2 段 EDITS 後以同一 xz 9e 重壓）。
再往前回 v631：同夾 dpr_rollback_v632_to_v631.py。"""
import sys, hashlib, base64, lzma, re
NEW_HEAD = '# -*- coding: utf-8 -*-\n"""dpr_suite.py — DPR 迴歸/迴路單檔套件（v633·1003 R-1003-3 T1 44 欄最終格式）\nv633（2026-10-03·**R-1003-3**·Amber 林彥博 P-1002-V7「比照」＝T1 追蹤表比照 T組 R-1002-25 改 44 欄（刪 AP、留 AN））：\n  · build_dpr.py v601→**v602**：AP 有無改以表頭判定（col40＝入庫夠數量時看 col41 是否「已完成訂單」），表頭無法判讀才回退欄數判定。\n    成因：T1 新 44 欄（有業務、無 AP）在舊判定下不補虛擬欄 → 助理欄讀到業務 #N/A，gate 23/23 仍綠（靜默錯）。\n    驗證：T1 10/2 表 45 欄重建與 v632 正式檔逐格相同；刪 AP 之 44 欄版只差主分析 AP 欄為空（與 T組 44 欄同型）。\n  · 其餘 11 檔、23 棒、快照 v579、字典 v95、NT/NS v513、overrides v1.11、判定式一行未動。SUITE_VERSION 632 → 633（R-v556-1）。\n  · 斷言端（44／45 欄 AP 判定之負向探針）與 v632 條目所記墊片斷言，均排下一個規格輪（快照 v580；v632 條目寫的「v576」為筆誤）。\n'
OLD_HEAD = '# -*- coding: utf-8 -*-\n"""dpr_suite.py — DPR 迴歸/迴路單檔套件（v632·1003 R-1003-2 xlrd 墊片取 Excel 快取值）\n'
EDITS = [('# FILE_VERSION = 602   # R-v555-1（Amber 0730「轉正」）：降版閘門用·改本檔須同步遞增\n# v602（2026-10-03·**R-1003-3**·Amber 林彥博 P-1002-V7「比照」＝T1 追蹤表比照 T組 R-1002-25 改 44 欄最終格式（刪 AP、留 AN））：\n#        AP 欄是否存在改以**表頭**判定（col40＝入庫夠數量時，看 col41 是否為「已完成訂單」）；表頭無法判讀才回退欄數判定。\n#        成因：舊式依檔名前綴契約欄數（T1＝44）判定，T1 新 44 欄（有業務、無 AP）會被當成「舊 44 欄有 AP」→ col41 下單月份錯位、\n#        助理欄讀到業務 #N/A（10/3 實測：A1／B3／4／6／6b／6c／派工 助理欄全變 #N/A，**gate 不報錯＝靜默錯**）。\n#        T組 44／45 欄、T1 45 欄行為不變（10/3 以 T1 10/2 表 45 欄與刪 AP 之 44 欄兩版建表逐格相同驗證）。判定式一行未動。\n', '# FILE_VERSION = 601   # R-v555-1（Amber 0730「轉正」）：降版閘門用·改本檔須同步遞增\n'), ("# R-1003-3（v602）：AP 有無改以表頭判定；表頭無法判讀才回退欄數判定（R-1001-16 原法）\ndef _hdr_at(i):\n    return _RAWH[COLMAP[i]].strip() if i < len(COLMAP) else ''\nif _hdr_at(40).startswith('入庫夠數量'):\n    AP_ABSENT, AP_SRC = (not _hdr_at(41).startswith('已完成訂單')), '表頭'\nelse:\n    AP_ABSENT, AP_SRC = (_EXPECT is not None and len(COLMAP) == _EXPECT - 1), '欄數回退'\nif AP_ABSENT:\n    COLMAP = COLMAP[:41] + [None] + COLMAP[41:]\n    print('  ℹ️ R-1001-16／R-1003-3：追蹤表已無 AP「已完成訂單」欄（判定來源：%s）→ col41 補空白虛擬欄（完成判定改讀 AO，不受影響）' % AP_SRC)\n", "AP_ABSENT = (_EXPECT is not None and len(COLMAP) == _EXPECT - 1)\nif AP_ABSENT:\n    COLMAP = COLMAP[:41] + [None] + COLMAP[41:]\n    print('  ℹ️ R-1001-16：追蹤表已無 AP「已完成訂單」欄 → col41 補空白虛擬欄（完成判定改讀 AO，不受影響）')\n")]   # (v602 文字, v601 文字)
src = open(sys.argv[1], encoding='utf-8').read()
assert src.startswith(NEW_HEAD) and src.count('SUITE_VERSION = 633') == 1, '輸入不是 v633'
m = re.search(r"^    'build_dpr.py': '([^']+)',$", src, re.M)
b = lzma.decompress(base64.b64decode(m.group(1))).decode('utf-8')
for n, o in EDITS:
    assert b.count(n) == 1
    b = b.replace(n, o, 1)
z = base64.b64encode(lzma.compress(b.encode('utf-8'), preset=9 | lzma.PRESET_EXTREME)).decode('ascii')
out = OLD_HEAD + src[len(NEW_HEAD):]
out = out.replace(m.group(0), "    'build_dpr.py': '%s'," % z, 1).replace('SUITE_VERSION = 633', 'SUITE_VERSION = 632', 1)
open(sys.argv[2], 'w', encoding='utf-8').write(out)
h = hashlib.sha256(out.encode('utf-8')).hexdigest()
print(h, '✅ v632' if h.startswith('0a090270') else '❌ 不符')
