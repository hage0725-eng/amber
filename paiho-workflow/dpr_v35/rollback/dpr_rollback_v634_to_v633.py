# -*- coding: utf-8 -*-
"""dpr_rollback_v634_to_v633.py — 把 dpr_suite.py v634 逐位元組還原成 v633（R-1002-26 E6 備份閘·R-1003-27）
用法：python3 dpr_rollback_v634_to_v633.py dpr_suite.py dpr_suite_v633.py
成功時印出 SHA256 3b2fe69f… ✅（v633 原檔）。再往前回 v632／v631 用同夾 dpr_rollback_v633_to_v632.py、dpr_rollback_v632_to_v631.py。
"""
import sys, re, json, base64, lzma, hashlib
EXPECT_IN = '522b1a1439c548c3e45b9f30892b75b9b300593cb36b9231ba16d06697428987'
EXPECT_OUT = '3b2fe69ff70928a42560d8cbfafd378ecbf435a16031d2c14707229254c6d6aa'
ES = json.loads('[["# -*- coding: utf-8 -*-\\n\\"\\"\\"dpr_suite.py — DPR 迴歸/迴路單檔套件（v634·1003 R-1003-27 報延天數表 NA 不顯示）\\nv634（2026-10-03·**R-1003-27**·Amber 林彥博「報延天數表·參數 Bảng ngày dời: NA直接刪掉」）：\\n  · build_dpr.py v602→**v603**：參數頁四張天數表的 NA 格改寫 =\\"\\"（顯示空白、保留灰底），頁尾色例「灰 NA」改「灰色空白」（中越）。\\n    A1 公式取到空字串仍為非數值 → 個案／上限，與 v602 行為相同。驗證：10/3 T組表 LibreOffice 重算後 A1 全頁 0 格差異；參數頁只差 559 個 NA 格＋1 格頁尾說明。\\n  · JSON 內部鍵仍為 \'NA\'（by_judge、第 23 棒 A19 不動）；其餘 11 檔、23 棒、快照 v579、字典 v95、NT/NS v513、overrides v1.11、判定式一行未動。SUITE_VERSION 633 → 634（R-v556-1）。\\n", "# -*- coding: utf-8 -*-\\n\\"\\"\\"dpr_suite.py — DPR 迴歸/迴路單檔套件（v633·1003 R-1003-3 T1 44 欄最終格式）\\n"], ["RETURN_3_SIDECAR = [\'dpr_tab_counts_latest.json\']   # 併同回傳·供下輪分頁棘輪比對\\nRETURN_3_LEGACY = [\'dpr_hash_registry.json\']   # 仍建議回傳·不列 WARN\\nSUITE_VERSION = 634   # R-v556-1（轉正·永久）：套件自版號（改 suite 必須同步改此常數）\\n", "RETURN_3_SIDECAR = [\'dpr_tab_counts_latest.json\']   # 併同回傳·供下輪分頁棘輪比對\\nRETURN_3_LEGACY = [\'dpr_hash_registry.json\']   # 仍建議回傳·不列 WARN\\nSUITE_VERSION = 633   # R-v556-1（轉正·永久）：套件自版號（改 suite 必須同步改此常數）\\n"]]')
EB = json.loads('[["\\n# FILE_VERSION = 603   # R-v555-1（Amber 0730「轉正」）：降版閘門用·改本檔須同步遞增\\n# v603（2026-10-03·**R-1003-27**·Amber 林彥博「報延天數表·參數 Bảng ngày dời: NA直接刪掉」）：\\n#        參數頁天數表 NA 格改寫 =\\"\\"（顯示空白、保留灰底）；A1 公式取到空字串仍非數值 → 個案／上限，判定與 v602 逐列相同。JSON 內部鍵仍為 \'NA\'，by_judge 不動。\\n", "\\n# FILE_VERSION = 602   # R-v555-1（Amber 0730「轉正」）：降版閘門用·改本檔須同步遞增\\n"], ["        for j_, k_ in enumerate(BY_KEYS):\\n            v_, s_, n_, p8_ = BY[\'tables\'][tn][p_][k_]\\n            c_ = put(wsBY, _r0 + 2 + i_, 2 + j_, (\'=\\"\\"\' if v_ == \'NA\' else v_),   # R-1003-27：NA 不顯示（=\\"\\" 空字串，A1 公式照舊判為非數值→個案）\\n", "        for j_, k_ in enumerate(BY_KEYS):\\n            v_, s_, n_, p8_ = BY[\'tables\'][tn][p_][k_]\\n            c_ = put(wsBY, _r0 + 2 + i_, 2 + j_, v_,\\n"], ["        BY_COLR = \'%s!$B$%d:$%s$%d\' % (BY_REF, _r0 + 1, _lastc, _r0 + 1)\\n    _r0 += len(BY_PRODS) + 3\\n_notes = [\'色：綠＝本品項實測（≥5 張）｜黃＝同品項合併／全產品實測｜白＝SOP v2.0｜灰色空白＝不經此站或無資料 → 提報。游標停在格子上看樣本數與 P80。 / \'\\n          \'Màu: xanh = thực đo cùng SP (≥5 đơn) | vàng = gộp cùng loại / toàn bộ SP | trắng = SOP v2.0 | ô xám để trống = không qua trạm hoặc không có dữ liệu → báo cáo. Rê chuột lên ô để xem số đơn và P80.\',\\n", "        BY_COLR = \'%s!$B$%d:$%s$%d\' % (BY_REF, _r0 + 1, _lastc, _r0 + 1)\\n    _r0 += len(BY_PRODS) + 3\\n_notes = [\'色：綠＝本品項實測（≥5 張）｜黃＝同品項合併／全產品實測｜白＝SOP v2.0｜灰 NA＝不經此站或無資料 → 提報。游標停在格子上看樣本數與 P80。 / \'\\n          \'Màu: xanh = thực đo cùng SP (≥5 đơn) | vàng = gộp cùng loại / toàn bộ SP | trắng = SOP v2.0 | xám NA = không qua trạm hoặc không có dữ liệu → báo cáo. Rê chuột lên ô để xem số đơn và P80.\',\\n"]]')
def rev(t, E, tag):
    for new, old in E:
        assert t.count(new) == 1, '%s 反向編修定位失敗' % tag
        t = t.replace(new, old, 1)
    return t
src, dst = sys.argv[1], sys.argv[2]
raw = open(src, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == EXPECT_IN, '輸入不是 v634（SHA256 不符）'
t = raw.decode('utf-8')
m = re.search(r"    'build_dpr\.py': '([A-Za-z0-9+/=]+)'", t)
b = lzma.decompress(base64.b64decode(m.group(1))).decode('utf-8')
b = rev(b, EB, 'build_dpr')
nb = base64.b64encode(lzma.compress(b.encode('utf-8'), preset=9 | lzma.PRESET_EXTREME)).decode('ascii')
t = t[:m.start(1)] + nb + t[m.end(1):]
t = rev(t, ES, 'suite')
out = t.encode('utf-8')
h = hashlib.sha256(out).hexdigest()
open(dst, 'wb').write(out)
print('SHA256', h[:8] + '…', '✅' if h == EXPECT_OUT else '❌ 不符')
sys.exit(0 if h == EXPECT_OUT else 1)
