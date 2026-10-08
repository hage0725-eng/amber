# -*- coding: utf-8 -*-
"""dpr_rollback_v636_to_v635.py — 把 dpr_suite.py v636 逐位元組還原成 v635（R-1002-26 E6 備份閘·R-1003-29）
用法：python3 dpr_rollback_v636_to_v635.py dpr_suite.py dpr_suite_v635.py
做法：從 v636 的 _PACK 取出回填字典 v97 → 5 筆 UP LTS 還原為 v96 原文、刪 map 2 鍵與 R-1003-29 規則／註記、還原 map_note 與版本
      → 重新編碼為 v96 放回 _PACK；再還原 docstring 與 SUITE_VERSION。成功時印出 SHA256 1aed2860… ✅（v635 原檔）。
"""
import sys, re, json, base64, lzma, hashlib, types
EXPECT_IN = '24ccc739db4e13ade1a797dfac91fae2027db8983f36b565a0b93a8210935e20'
EXPECT_OUT = '1aed286042e512ac40d970494d635dcbe40441f77b2a500bcb088186496cbfd5'
DOC_NEW = '"""dpr_suite.py — DPR 迴歸/迴路單檔套件（v636·1003 R-1003-29 UP LTS 歸異常未交）\nv636（2026-10-03·**R-1003-29**·Amber 林彥博「P-1003-T8:按建議」）：\n  · 回填字典 v96→**v97**：b3_replies 5 筆「ĐƠN BÁO CÁO UP LTS」其他→**異常未交**（過渡期）；map +2（DON BAO CAO UP LTS／DON CAN BAO CAO UP LTS→異常未交）。\n    第四類「待 LTS 報告」排下一個規格輪（R-1003-24）。只換 _PACK 字典；builder v603、23 棒、快照 v579、判定式一行未動。SUITE_VERSION 635 → 636（R-v556-1）。\n'
DOC_OLD = '"""dpr_suite.py — DPR 迴歸/迴路單檔套件（v635·1003 R-1003-28 T組 1002 回填攝取）\n'
VER_NEW, VER_OLD = 'SUITE_VERSION = 636   #', 'SUITE_VERSION = 635   #'
MAP_NOTE_OLD = '正規化（去聲調·大寫·去標點）後精確比對；三選一中越原文 6 句＋CHUA TOI ETD NGAY GIAO KH（Claude 對譯為「未到客戶交期」·**Amber 0928 確認**「未到交期，未到期不要詢問」R-0928-8）。未命中＝其他（保留原文、請改填三選一）；**R-1003-28（Amber 10/3）**：CHƯA ĐẾN NGAY GIAO ĐỢI BQ（BQ＝報關 báo quan）→ 未到出貨日＝未到客戶交期'
ORIG_ITEMS = json.loads('{"DGT-20260612A-2FT#11": {"reply": "ĐƠN BÁO CÁO UP LTS", "class": "其他", "date": "2026-10-02", "okh_at_reply": "2026/06/27", "cust": "011580", "source": "T組進度完整分析_1002.xlsx（Amber 2026-10-03「回填更新」回傳·SHA256-8 24f7e10d） B3", "ingest": "R-1003-28", "status_at_reply": "⚠️已過回復客戶日·未交 / Quá ngày hẹn KH, chưa giao", "note": "LTS＝Deckers 集團報告上傳系統；DGT 訂單測試報告上傳 LTS 後才能結案（Amber 10/3）。三選一類別待 Amber 指定"}, "DGT-20260612A-1FT#11": {"reply": "ĐƠN BÁO CÁO UP LTS", "class": "其他", "date": "2026-10-02", "okh_at_reply": "2026/06/27", "cust": "011580", "source": "T組進度完整分析_1002.xlsx（Amber 2026-10-03「回填更新」回傳·SHA256-8 24f7e10d） B3", "ingest": "R-1003-28", "status_at_reply": "⚠️已過回復客戶日·未交 / Quá ngày hẹn KH, chưa giao", "note": "LTS＝Deckers 集團報告上傳系統；DGT 訂單測試報告上傳 LTS 後才能結案（Amber 10/3）。三選一類別待 Amber 指定"}, "DGT-20260804A-8CT#11": {"reply": "ĐƠN BÁO CÁO UP LTS", "class": "其他", "date": "2026-10-02", "okh_at_reply": "2026/08/20", "cust": "011580", "source": "T組進度完整分析_1002.xlsx（Amber 2026-10-03「回填更新」回傳·SHA256-8 24f7e10d） B3", "ingest": "R-1003-28", "status_at_reply": "📦保留足·已過回復客戶日·未交 / Bảo lưu đủ, quá hẹn KH（報告未到）", "note": "LTS＝Deckers 集團報告上傳系統；DGT 訂單測試報告上傳 LTS 後才能結案（Amber 10/3）。三選一類別待 Amber 指定"}, "DGT-20260804A-9CT#11": {"reply": "ĐƠN BÁO CÁO UP LTS", "class": "其他", "date": "2026-10-02", "okh_at_reply": "2026/08/20", "cust": "011580", "source": "T組進度完整分析_1002.xlsx（Amber 2026-10-03「回填更新」回傳·SHA256-8 24f7e10d） B3", "ingest": "R-1003-28", "status_at_reply": "📦保留足·已過回復客戶日·未交 / Bảo lưu đủ, quá hẹn KH（報告未到）", "note": "LTS＝Deckers 集團報告上傳系統；DGT 訂單測試報告上傳 LTS 後才能結案（Amber 10/3）。三選一類別待 Amber 指定"}, "DGT-H411400349-180#11": {"reply": "ĐƠN BÁO CÁO UP LTS", "class": "其他", "date": "2026-10-02", "okh_at_reply": "2026/09/10", "cust": "011581", "source": "T組進度完整分析_1002.xlsx（Amber 2026-10-03「回填更新」回傳·SHA256-8 24f7e10d） B3", "ingest": "R-1003-28", "status_at_reply": "⚠️已過回復客戶日·未交 / Quá ngày hẹn KH, chưa giao", "note": "LTS＝Deckers 集團報告上傳系統；DGT 訂單測試報告上傳 LTS 後才能結案（Amber 10/3）。三選一類別待 Amber 指定"}}')
src, dst = sys.argv[1], sys.argv[2]
raw = open(src, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == EXPECT_IN, '輸入不是 v636（SHA256 不符）'
t = raw.decode('utf-8')
blob = lambda n: re.search(r"    '%s': '([A-Za-z0-9+/=]+)'" % re.escape(n), t)
codec = types.ModuleType('dict_v14_codec')
exec(lzma.decompress(base64.b64decode(blob('dict_v14_codec.py').group(1))).decode('utf-8'), codec.__dict__)
m = blob('回填原因處置字典_v97_columnar.json')
D = codec.decode(json.loads(lzma.decompress(base64.b64decode(m.group(1))).decode('utf-8')))
b3 = D['b3_replies']
for k, v in ORIG_ITEMS.items(): b3['items'][k] = v
for k in ('DON BAO CAO UP LTS', 'DON CAN BAO CAO UP LTS'): del b3['map'][k]
b3['map_note'] = MAP_NOTE_OLD
assert b3['rulings'][-1]['rule'] == 'R-1003-29'; b3['rulings'].pop()
del D['rule_R_1003_29']; del D['note_v97']; D['version'] = 'v96'
p = json.dumps(codec.encode(D), ensure_ascii=False, separators=(',', ':')).encode('utf-8')
b = base64.b64encode(lzma.compress(p, preset=9 | lzma.PRESET_EXTREME)).decode('ascii')
t = t[:m.start()] + "    '回填原因處置字典_v96_columnar.json': '" + b + "'" + t[m.end():]
assert t.count(DOC_NEW) == 1 and t.count(VER_NEW) == 1
t = t.replace(DOC_NEW, DOC_OLD, 1).replace(VER_NEW, VER_OLD, 1)
out = t.encode('utf-8'); h = hashlib.sha256(out).hexdigest()
open(dst, 'wb').write(out)
print('SHA256', h[:8] + '…', '✅' if h == EXPECT_OUT else '❌ 不符')
sys.exit(0 if h == EXPECT_OUT else 1)
