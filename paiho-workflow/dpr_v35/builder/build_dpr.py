
# FILE_VERSION = 587   # R-v555-1（Amber 0730「轉正」）：降版閘門用·改本檔須同步遞增
#   v585（2026-09-17）：R-0917-24（Amber 0917「Chua HC=訂單數量-完工數量，跟訂單單位一致，
#        僅做為是否需要追蹤進度輔助判定使用」）—— **純載入層**。
#        成因：9/17 T組追蹤表在 col22 新增 ERP 欄 `CHUA HC`（46 欄），撞 45 欄契約硬斷言。
#        處置：讀檔時以**表頭名稱**剔除 DROP_COLS 之欄，還原契約欄序；不新增任何輸出欄。
#        立論：Amber 定義 CHUA HC ＝ 數量 − 完工量，兩欄皆已在契約內 → 該欄 100% 可導出、
#        剔除零資訊損失（0917 實測 10,730/10,730 逐列相符、0 例外）。且該欄為助理端輔助判定用，
#        非本表任何判定式之輸入 —— **異常判定式一行未動**。
#        負向驗證：46欄→剔除後45欄可建｜45欄原檔→COLMAP 全等 range(45)·輸出逐格相同｜
#        44欄 T1 舊契約→不受影響｜欄名變動（如 CHUA_HC）→不剔除、仍由契約斷言擋下不靜默。
#   v584（2026-09-16）：Amber 0916「H1-是（限抓取期間·不含跨組別）」＋「H2-做」兩項 ——
#        ⒜ R-0916-35：89DB 累積檔改**依組別擇檔**（`89DB_累積_<組>.xlsx` > `89DB_累積.xlsx`）
#           並讀 `_scope` 分頁驗證組別；組別不符一律不採（視同缺檔）。覆蓋率閘門只看日期不看組別，
#           拿 T1 的累積檔算 T組會錯判為已覆蓋 —— 此為該風險之守門。
#        ⒝ R-0916-36：4s.共用89餘量不足 **作用態實作**（原為硬編碼佔位）。判定＝多張正式單掛同一張 89
#           （同料號/色號/寬度/型號）且合計未交 ＞ 89 未交；分攤依 R-v500-1 FIFO（下單日序·吃不下
#           就跳過續看）；單位不一致者不加總、標人工判定。未達 R-v527-1 覆蓋率者維持佔位（不變）。
#        主分析異常判定式一行未動 —— DELAY/WARNING/POTENTIAL/OK 與 OTD 必須與 v583 逐格相同。
#   v583（2026-09-16）：R-0916-29（Amber 0916「T1-K 只加一個提示欄」·純呈現層）——
#        4.應掛未掛 新增「同89合計檢查」欄：同一張 89（單號＋序號）被幾個群共用、
#        正式單合計未交 vs 該 89 未交量是否超額。R-v528-3 逐群判定式一行未動，
#        群數／列數／豁免計數／所有其他分頁數字必須與 v582 逐格相同。
#        欄位契約：4.應掛未掛 不在 v494 CONTRACT 等值清單內（僅查 群組#／列別／BF五欄／未交數量），
#        新欄置於「未交量判定」與「下單日」之間，不影響任何既有斷言 → **未改任何迴歸棒**。
#   v582（2026-09-16）：Amber 林彥博 0916「T1-A 確認授權」＋「T1-F 是·納入同一支 v582」兩項 ——
#        ⒜ R-0916-19：組別判定改「輸入檔名前綴為第一鍵、欄數為第二鍵」。0916 之 T1 追蹤表已改為
#           45 欄含業務欄，與 T組契約相同，欄數判組必然誤判並覆蓋同日 T組交付檔（靜默無報錯）。
#        ⒝ R-0916-20：T1組客戶清冊改 glob 擇優（候選 '*T1 客戶清冊*'>'*T1組客戶清冊*'，兩側包 *
#           以容忍 PROJECT 上傳序號前綴，比照 R-0916-16b）。與 R-0916-3 同型同級。
#        兩項皆為**純載入／標籤層**，異常判定式一行未動 —— DELAY/WARNING/POTENTIAL/OK 與 OTD
#        在「同輸入、同清冊」條件下必須逐格相同。
#   v579（2026-09-16）：Amber 林彥博 0916 兩項授權 —— 皆為**純載入／白名單層**，異常判定式一行未動。
#   v581（2026-09-16）：R-0916-16b —— 品牌主檔 glob 容忍「上傳前綴」與 CSV/TSV 副檔。
#        成因：0916 回傳之品牌清冊在 PROJECT 實際落檔名為 `1789530326906_品牌代號清冊 9.16.XLS`
#        （帶上傳序號前綴），且以「文字萃取 doc」而非 blob 保存 → v580 之 glob 與 xlrd 皆取不到。
#        處置：候選改為含 * 前綴之樣式並支援 .csv/.tsv 文字副本。純載入層，判定式一行未動。
#   v580（2026-09-16）：R-0916-16（Amber 0916「E5-品牌主檔 glob 擇優授權」）—— 品牌主檔改 **glob 擇優**。
#        成因與 R-0916-3 同型：0916 新版品牌清冊以 `品牌代號清冊 9.16.XLS` 之名回傳，
#        硬讀 `brands品牌代碼對照表.XLS` 會靜默取到 PROJECT 內 5/23 舊版（403 碼·PM 已換手）。
#        處置：候選 ('品牌代號清冊*.XLS','brands品牌代碼對照表.XLS') 以「表頭命中 BRAND_COLS 數」為第一鍵、
#        候選順序為第二鍵；全缺則 raise，不靜默 fallback。純載入層，判定式一行未動。
#     ⒜ R-0916-3（D1⒝「授權 build_dpr.py v578→v579 純載入層改動」）：T組客戶清冊改 **glob 擇優**。
#        背景：0911 回傳之原始檔名為 `T組客戶.XLS`，與 PROJECT 內既有 `T組客戶清冊.XLS` 不同名 →
#        兩檔並存時硬讀舊名會靜默取到 5/23 舊版（0912／0915 兩輪皆中，R-0915-4／R-0916-2 留痕）。
#        處置：候選 ('T組客戶.XLS','T組客戶清冊.XLS') 以「表頭命中 ROSTER_COLS 數」為第一鍵、
#        名稱優先序為第二鍵擇優；選中者列印留痕。找不到任何候選才報錯（不靜默回退）。
#     ⒝ R-0916-4（Amber 0916「C5入白名單」）：7w.品牌空白 新增**字典驅動之抑制白名單**
#        brand_code_overrides_v1_1.json → suppress_7w。名列者不進 7w 計數，但於分頁末段具名列示
#        （**抑制不等於隱藏**：白名單本身要看得見，否則下次無人記得為何不報）。
#   v578（2026-09-11）：R-0911-9（Amber 林彥博 0911「更新客戶代碼設定」）客戶清冊改**表頭定位**——
#                      0911 新版 T組客戶清冊由 22 欄擴為 68 欄，業務/助理/品牌 欄序 7/8/9 → 10/11/13。
#                      原寫死欄序照跑會把 141 筆之業務/助理/品牌整批讀成地址字串（靜默誤判）。
#                      純載入層變更，**異常判定式一行未動** —— DELAY/WARNING/POTENTIAL/OK 與 OTD 必須逐格相同。
#   v577（2026-09-08）：R-0908-4（Amber 林彥博 0908 於 6b 具名裁決「合理回報，請結案不要再複查」）——
#                      新增字典驅動之 R-0819-1 復檢個案豁免清單 no_recheck_orders：
#                      名列其中之 89 已結案且經 Amber 具名審閱者，不再回列 6b 復檢，改走 9.已結案移除。
#                      **R-0819-1 規則本身未更動**（仍為轉正·永久），本項為逐單個案豁免（R-0819-2 不泛化）。
#                      異常判定式一行未動 —— DELAY/WARNING/POTENTIAL/OK 與 OTD 必須逐格相同。
#   v576（2026-09-08）：R-0908-1（Amber 林彥博 0908「2.統計／2b.產品別準交率 只要是百分比的欄位
#                      都一律顯示為 _%」）—— 純呈現層：百分比儲存格加 number_format '0.0"%"'，
#                      **值本身不變（仍為 60.6 之數值·可排序可篩選）**，只是顯示為 60.6%。
#                      異常判定式與 OTD 計算一行未動 —— 逐格數值必須與 v575 完全相同。
#   v575（2026-09-04）：R-0904-2 製程站別對照表補冊（92卷紗／94染色／96打束頭／98特殊加工）＋
#                      R-0904-3 分頁順序改「須人工回填者置前」（Amber 林彥博 0904 兩項指示）。
#                      新增：1.主分析「今日站別」欄（append·不動既有欄序）、2.統計「製程站別 × 異常等級」區塊。
#                      異常判定式一行未動 —— DELAY/WARNING/POTENTIAL/OK 與 OTD 必須逐格相同。
#   v574（2026-09-03）：R-0903-1（Amber 0903「A1-b」）字典 glob 接受 .json.gz（PROJECT 空間所迫）。
#                      純載入層變更，判定邏輯一行未動（輸出數字必須逐格相同）。
#   v573（2026-08-26）：Amber 林彥博 四項轉正裁決落地（A1 R-0819-1／A2 R-0820-1／
#                      A3 R-v563-1／A4 R-v568-2）—— 全部由「暫行」改「轉正·永久」。
#                      純登錄冊/文案層變更，判定邏輯一行未動（輸出數字必須逐格相同）。
#   v572（2026-08-20）：R-0820-1 觀察到期自動落回 6 表（Amber 0820「落回」）·改列派工強制。
#   v571（2026-08-19）：R-0819-8 裁決待辦（pending_action）自動入派工強制列。
#   v570（2026-08-19）：R-0819-7 —— 99Z 家族（特殊品名/加工單號）不得入 8.NTNS未分類；
#                      1.主分析 NT/NS 欄標示「特殊品名/加工單號·不列NT/NS」。
#   v569（2026-08-19）：R-0819-1 結案後復檢回列 6b＋新增 6c.重複備料曝險（垂直並列）；
#                      NT/NS 留白清單改讀字典 protected.pending_blank；6b 新增♻️復檢/原結案處置兩欄。
# -*- coding: utf-8 -*-
"""build_dpr.py v568 — T組 DPR 通用建構器（PROJECT FILES 同名檔工作副本）"""
import datetime
import glob as _glob
import math
import pickle
import re
import sys

import xlrd

sys.path.insert(0, '/home/claude/dpr')
from dict_v14_codec import load_any
import dpr_regression_live_common as lc

import sys as _sys
INPUT = _sys.argv[1] if len(_sys.argv) > 1 else 'T組追蹤進度表_7_15.XLS'
_m = re.search(r'_(\d{1,2})_(\d{1,2})\.XLSX?$', INPUT, re.I)
assert _m, '輸入檔名須含 _M_D.XLS 日期段'
TODAY = datetime.date(2026, int(_m.group(1)), int(_m.group(2)))
WAVE_DATE = (TODAY + datetime.timedelta(days=1)).isoformat()
MMDD = TODAY.strftime('%m%d')
WAVE_MMDD = (TODAY + datetime.timedelta(days=1)).strftime('%m-%d')
DUE_FORCE = (TODAY + datetime.timedelta(days=1)).strftime('%Y/%m/%d')
DUE_NORM = (TODAY + datetime.timedelta(days=3)).strftime('%Y/%m/%d')
EPOCH = datetime.date(1899, 12, 30)
ILLEGAL = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f]')

# ══ R-0904-2（Amber 林彥博 2026-09-04·轉正·永久）製程站別對照表補冊 ══
# amber_ruling：「92-=卷紗／94-=染色／96-=打束頭／98-=特殊加工(具體加工類型看子代碼)」
# 背景：92/94/96/98 自 0903 起連三輪列「待確認·不臆測」（本輪前 1,374 筆·35.0% 無站別可判）。
# 本輪由 Amber 逐碼裁定後入冊 → 待確認歸零，製程站別風險加權自本輪起可用。
# 98 之具體加工類型須看子代碼，故 98 一律附掛子代碼原文，不再往上歸併。
PROC_STATION = {
    '92': '卷紗 / Đánh suốt',
    '93': '織造 / Dệt',
    '94': '染色 / Nhuộm',
    '95': '胚帶後製程 / Hoàn thiện',
    '96': '打束頭 / Bấm đầu dây',
    '97': '品檢包裝 / KCS & đóng gói',
    '98': '特殊加工 / Gia công đặc biệt',
}
PROC_SRC = {'92': 'R-0904-2', '94': 'R-0904-2', '96': 'R-0904-2', '98': 'R-0904-2'}
PROC_BLANK = '無今日進度紀錄 / Chưa có tiến độ hôm nay'
PROC_UNKNOWN = '待確認·不臆測 / Cần xác nhận'
_PROC_RE = re.compile(r'^\s*(\d{2})-([A-Za-z0-9]*)')


def station_of(prog):
    """由進度欄字串取製程站別。R-0904-2：98 附掛子代碼；未在對照表者標待確認·不臆測。"""
    t = dnz(prog)
    if not t or t in ('0', '0:00:00'):
        return PROC_BLANK
    m = _PROC_RE.match(t)
    if not m:
        return PROC_UNKNOWN
    code, sub = m.group(1), m.group(2)
    name = PROC_STATION.get(code)
    if not name:
        return PROC_UNKNOWN
    if code == '98' and sub:
        return '%s·子代碼 %s' % (name, sub)
    return name


def dnz(x):
    if x is None:
        return ''
    if isinstance(x, float):
        return '' if math.isnan(x) else (str(int(x)) if x == int(x) else str(x))
    s = str(x).strip()
    return ILLEGAL.sub('', s)


UNDEL_HDR = '未交數量 / SL chưa giao'     # R-v561-1（Amber 林彥博 2026-08-03）
UNIT_RULED = {'碼': 'Y', '米': 'M', '雙': 'Pair', 'PC': 'PC',
              'Y': 'Y', 'M': 'M', 'PAIR': 'Pair'}
UNDEL_MIN = 200                            # R-v561-2 門檻

# ══ R-0918-8（Amber 林彥博 2026-09-18·轉正）計量單位換算 ══
# 裁示原文：「長度換長度、重量換重量、個數換個數，這些可以直接換算；不同的計算類型要看實際用量表才能換算，
#   但可以用89累積表裡面的實秤重量去轉換（必需確保同品名/規格）」「雙=2pcs，但也可能有例外，例如一雙鞋用到四片，例外則特案處理」
# 取代 R-v561-1／R-0916-7「單位不一致不可換算」之舊旨（僅轄 Sheet4 與 4s 之未交量對照）。
UNIT_FAMILY = {'碼': ('LEN', 0.9144), 'Y': ('LEN', 0.9144), '米': ('LEN', 1.0), 'M': ('LEN', 1.0),
               '雙': ('CNT', 2.0), 'PAIR': ('CNT', 2.0), 'PC': ('CNT', 1.0), 'PCS': ('CNT', 1.0),
               'KG': ('WT', 1.0), 'G': ('WT', 0.001)}
FAM_ZH = {'LEN': '長度', 'CNT': '個數', 'WT': '重量'}
WT_KGPU = {}   # (料號,寬度,型號) → {單位: 每單位實秤淨重KG}；由 89 累積檔之實秤欄建立（無則空）


def conv_qty(qty, ufrom, uto, spec=None):
    """R-0918-8：回傳 (換算值, 說明)；不可換算回 (None, 原因)。"""
    a, b = dnz(ufrom).upper(), dnz(uto).upper()
    if not a or not b:
        return None, '單位空白'
    if a == b:
        return qty, ''
    fa, fb = UNIT_FAMILY.get(a), UNIT_FAMILY.get(b)
    if fa and fb and fa[0] == fb[0]:
        v = round(qty * fa[1] / fb[1], 3)
        how = '%s換算 %s%s→%s%s' % (FAM_ZH[fa[0]], qty, dnz(ufrom), v, dnz(uto))
        if fa[0] == 'CNT' and ('PAIR' in (a, b) or '雙' in (a, b)):
            how += '·雙=2PC預設（一雙多片等例外特案處理）'
        return v, how + '(R-0918-8)'
    kg = WT_KGPU.get(spec or ())
    if kg:
        ka = kg.get(a) if not (fa and fa[0] == 'WT') else fa[1]
        kb = kg.get(b) if not (fb and fb[0] == 'WT') else fb[1]
        if ka and kb:
            v = round(qty * ka / kb, 3)
            return v, '實秤換算(同品名/規格·89累積表) %s%s→%s%s(R-0918-8)' % (qty, dnz(ufrom), v, dnz(uto))
    return None, '跨計量類別(%s↔%s)·無同規格實秤資料' % (
        FAM_ZH.get((fa or ('?',))[0], '未裁決'), FAM_ZH.get((fb or ('?',))[0], '未裁決'))


def undel(r):
    """R-v561-1：未交數量＝數量(col15) − 已交(col21)，原生單位。
    amber_ruling（Amber 林彥博 2026-08-03）：**不得用「未交折合碼」(col22) 對照** ——
    該欄已折算為碼（米×1.1／雙×2.4／PC×0.164），與原生單位之訂單數量不可比。"""
    return round(fnum(r[15]) - fnum(r[21]), 3)


def unit_of(r):
    return UNIT_RULED.get(dnz(r[16]).upper(), '')


def fnum(v):
    try:
        f = float(v)
        return 0.0 if math.isnan(f) else f
    except Exception:
        return 0.0


def as_date(v):
    f = fnum(v)
    if f > 20000:
        try:
            return EPOCH + datetime.timedelta(days=int(f))
        except Exception:
            return None
    return None


def dstr(v):
    d = as_date(v)
    return d.strftime('%Y/%m/%d') if d else ('0' if fnum(v) == 0 and dnz(v) in ('', '0') else dnz(v))


# ---------- R-v551-2：ERP 天數欄三態編碼 ----------
ERP_DAYS_COLS = (36, 37, 38)
ERP_DEGENERATE_MIN = 365          # > 365 ＝ TODAY() 退化序號


def erp_days(v):
    """回傳 (state, days)：state ∈ {'no_base','ontime','over'}；僅 'over' 帶天數。"""
    s = dnz(v)
    if s == '-':
        return ('ontime', None)
    if s in ('', '0'):
        return ('no_base', None)
    f = fnum(v)
    if f > ERP_DEGENERATE_MIN:
        return ('no_base', None)
    if f > 0:
        return ('over', math.floor(f))
    return ('ontime', None)


# ---------- R-v566-1：準交率 OTD 引擎（內部從嚴 L2） ----------
FILE_VERSION = 574
OTD_GRACE_DAYS = 2
OTD_MIN_N = 5


def otd_of(r, ordered_date=None):
    """回傳 (in_cohort: bool, ontime: bool|None, basis: str)。"""
    s19 = erp_days(r[37])
    s36 = erp_days(r[36])
    has19 = dnz(r[6]) not in ('', '0')
    if has19 and s19[0] != 'no_base':
        return (True, s19[0] == 'ontime', '1.9')
    if not has19:
        if ordered_date is not None and (TODAY - ordered_date).days <= OTD_GRACE_DAYS:
            return (False, None, 'grace')
        if s36[0] != 'no_base':
            return (True, s36[0] == 'ontime', 'STD')
        return (False, None, 'no_base')
    if s36[0] != 'no_base':
        return (True, s36[0] == 'ontime', 'STD')
    return (False, None, 'no_base')


def otd_rate(rows):
    d = [x for x in rows if x[0]]
    n = sum(1 for x in d if x[1])
    return (len(d), n, (n / len(d)) if d else None)


# ---------- 1. preflight ----------
PRE = lc.preflight(strict=False)
assert PRE['snapshot_version'] >= 525 and PRE['dict_version'] >= 24 and PRE['whitelist_active_entries'] == 0, \
    'E-4 硬斷言不符：' + '；'.join(PRE['errors'])
SHEET4_ENABLED = PRE['sheet4_enabled']
print('preflight:', PRE['preflight_pass'], '| snapshot v%d dict v%d 白名單活性%d | 89區間檔 %d/12 → sheet4_enabled=%s'
      % (PRE['snapshot_version'], PRE['dict_version'], PRE['whitelist_active_entries'],
         PRE['interval_89_files'], SHEET4_ENABLED))

# ---------- 2. 載入原始表＋去重 ----------
wbx = xlrd.open_workbook(INPUT)
sh = wbx.sheet_by_name('統整')
# ══ R-0917-24（Amber 林彥博 2026-09-17·純載入層）ERP 新增欄以**表頭名稱**剔除 ══
# 只剔除「可由契約內既有欄 100% 導出、且非任何判定式輸入」之欄。新增名單須具名裁示。
DROP_COLS = ('CHUA HC',)          # ＝ 數量 − 完工量（Amber 0917 定義）·助理端追蹤輔助欄
_RAWH = [dnz(sh.cell_value(0, c)) for c in range(sh.ncols)]
COLMAP = [c for c in range(sh.ncols) if _RAWH[c] not in DROP_COLS]
_DROPPED = [(c, _RAWH[c]) for c in range(sh.ncols) if _RAWH[c] in DROP_COLS]
if _DROPPED:
    print('  ℹ️ R-0917-24 載入層剔欄：%s（原 %d 欄 → %d 欄）'
          % (['col%d=%s' % (c, h) for c, h in _DROPPED], sh.ncols, len(COLMAP)))
NCOLS = len(COLMAP)
assert NCOLS in (44, 45), f'欄數 {NCOLS} 非 T組(45)/T1組(44) 契約（剔欄後·R-0917-24）'
# ══ R-0916-19（Amber 林彥博 2026-09-16「T1-A 確認授權」·純標籤層）組別判定改檔名前綴優先 ══
# 成因：0916 之 T1組追蹤進度表已改為 45 欄且 col44 帶「業務 / nghiệp vụ」表頭，
#   與 T組契約完全相同 → 原「欄數判組」必然把 T1 判成 T組，輸出檔名與封面標題皆錯，
#   且會覆蓋同日 T組交付檔（靜默、無報錯）。
# 處置：①輸入檔名前綴（T1組／T1／T組）為第一鍵 ②欄數為第二鍵（前綴無法判讀時沿用舊法）。
#   GROUP 僅用於列印／封面標題／輸出檔名／manifest 之 group 欄 —— **判定式一行未動**。
_INBASE = INPUT.split('/')[-1]
if re.match(r'^T1[組\s_\-]', _INBASE):
    IS_T1, GROUP_SRC = True, '檔名前綴 T1'
elif re.match(r'^T[組\s_\-]', _INBASE):
    IS_T1, GROUP_SRC = False, '檔名前綴 T'
else:
    IS_T1, GROUP_SRC = (NCOLS == 44), '欄數回退（檔名無組別前綴）'
GROUP = 'T1組' if IS_T1 else 'T組'
HDR = [dnz(sh.cell_value(0, c)) for c in COLMAP]
print('  ℹ️ 組別判定＝%s（來源：%s·欄數 %d·R-0916-19）' % (GROUP, GROUP_SRC, NCOLS))
assert NCOLS == 44 or HDR[44].startswith('業務'), '45 欄契約應含業務欄(col44)'
rows_raw = []
for r in range(1, sh.nrows):
    rows_raw.append([sh.cell_value(r, c) for c in COLMAP])
n_raw = len(rows_raw)
DEDUP_KEY_COLS = (2, 3, 11, 12, 0)   # 訂單號碼, #2, 料號, 色號, 類別
seen, rows, _dropped = set(), [], []
for r in rows_raw:
    k = tuple(dnz(r[c]) for c in DEDUP_KEY_COLS)
    if k in seen:
        _dropped.append(dnz(r[2]))
        continue
    seen.add(k)
    rows.append(r)
n_dedup = len(rows)
if _dropped:
    from collections import Counter as _C
    print('  去重剔除（R-v552-1 新鍵）：', dict(_C(_dropped)))
active = [r for r in rows if dnz(r[41]) != '✔']
n89 = sum(1 for r in active if dnz(r[0]) == '89')
print(f'{GROUP}：原始 {n_raw} → 去重 {n_dedup}（−{n_raw-n_dedup}）→ active {len(active)}（89={n89}）')

POP89_ABSENT = (n89 == 0)
HALT563 = ('⛔ 停判 TẠM DỪNG PHÁN ĐỊNH（R-v563-1·Amber 0826 轉正·永久）：本輪輸入檔不含 89 預告母體'
           '（類別=89 計 0 列）→ 4／4s／6／6觀察／6b／9 六表停判。'
           '**0 列 ≠ 無異常**，僅表示無法判定。'
           '處理：請重新匯出「含 89 預告單」之進度表，當輪重跑並回報差異。'
           ' / File tiến độ kỳ này KHÔNG có đơn dự báo 89 → 6 bảng vòng đời 89 TẠM DỪNG phán định. '
           '0 dòng KHÔNG có nghĩa là không có bất thường. Đây là vấn đề dữ liệu đầu vào, KHÔNG tính lỗi trợ lý.')
if POP89_ABSENT:
    print('⛔ R-v563-1 停判：89 母體=0')

# ---------- 3. 富化 ----------
import json as _json

NV_VI = {
    '黎文慶': '黎文慶 / Lê Văn Khánh',
    '阮豪創': '阮豪創 / Nguyễn Hào Sáng',
    '阮紅杏': '阮紅杏 / Nguyễn Hồng Hạnh',
    '林彥博': '林彥博 / Amber Lin',
    '阮智賢': '阮智賢 / Nguyễn Trí Hiền',
    '阮氏玉欣': '阮氏玉欣 / Nguyễn Thị Ngọc Hân',
    # R-v551-1 續（Amber 2026-07-28「助理越名確認」·轉正·永久）：助理 12 位正名
    # 溯源法：ERP 對同一助理時而輸出中文時而越文 → 以「客戶代碼集合重疊」配對＋漢越音逐字交叉驗證。
    # 紀律：能溯源就不音譯；音譯僅在來源檔完全無越文對應時作候選提交；未命中一律掛 fallback，禁臆測。
    '何雪蓉': '何雪蓉 / Hà Tuyết Nhung',
    '楊氏燕兒': '楊氏燕兒 / Dương Thị Yến Nhi',
    '泰林錦玉': '泰林錦玉 / Thái Lâm Cẩm Ngọc',
    '道芳紅絨': '道芳紅絨 / Đào Phương Hồng Nhung',
    '長黃玉莉': '長黃玉莉 / Trương Hoàng Ngọc Ly',
    '阮氏喬義': '阮氏喬義 / Nguyễn Thị Kiều Nghĩa',
    '阮氏黃郊': '阮氏黃郊 / Nguyễn Thị Huỳnh Giao',
    '陳婷清竹': '陳婷清竹 / Trần Đình Thanh Trúc',
    '陳氏明莊': '陳氏明莊 / Trần Thị Minh Trang',
    '陳氏燕兒': '陳氏燕兒 / Trần Thị Yến Nhi',
    '黎氏艷莊': '黎氏艷莊 / Lê Thị Diễm Trang',
    '黎氏黃燕': '黎氏黃燕 / Lê Thị Hoàng Yến',
}
_VI_RE = re.compile(r'[a-zA-ZÀ-ỹĐđ]')


def nv_bi(name):
    n = dnz(name)
    if not n:
        return ''
    if _VI_RE.search(n):
        return n
    return NV_VI.get(n, n + ' / (chờ chuẩn hóa tên VI)')


# ══ R-0911-9（Amber 林彥博 2026-09-11「更新客戶代碼設定」）客戶清冊改表頭定位 ══
# 背景：0911 回傳之 T組客戶清冊由 22 欄擴為 68 欄（新增開票/聯繫/授信等欄位），
#   業務 7→10、助理 8→11、品牌 9→13 全數位移。原寫死欄序若照跑，
#   141 筆客戶之業務/助理/品牌會**整批讀成地址字串**——不報錯、外觀正常、數字全錯
#   （與 R-v551-2／R-0827-4 同型之靜默誤判）。
# 落地：改以**表頭名稱定位**（找不到表頭才回退舊欄序），新舊版清冊皆可讀。
#   純載入層變更，判定邏輯一行未動（比照 R-0903-1 字典 glob 變更之先例）。
ROSTER_COLS = ('客戶代碼', '客戶簡稱', '業務', '助理', '品牌')
ROSTER_FALLBACK = {'客戶代碼': 0, '客戶簡稱': 3, '業務': 7, '助理': 8, '品牌': 9}


def read_roster(path):
    w = xlrd.open_workbook(path)
    s = w.sheet_by_index(0)
    hdr = [dnz(s.cell_value(0, c)) for c in range(s.ncols)]
    idx, missing = {}, []
    for want in ROSTER_COLS:
        if want in hdr:
            idx[want] = hdr.index(want)
        else:
            idx[want] = ROSTER_FALLBACK[want]
            missing.append(want)
    if missing:
        print('  ⚠️ 客戶清冊 %s 缺表頭 %s → 回退舊欄序（R-0911-9）' % (path, missing))
    elif [idx[c] for c in ROSTER_COLS] != [ROSTER_FALLBACK[c] for c in ROSTER_COLS]:
        print('  ℹ️ 客戶清冊 %s 欄位已位移，改表頭定位（R-0911-9）：%s'
              % (path, {c: idx[c] for c in ROSTER_COLS}))
    out = {}
    for i in range(1, s.nrows):
        code = dnz(s.cell_value(i, idx['客戶代碼']))
        if code and code.replace('-', '').isdigit():
            code = code.zfill(6)
        out[code] = {'簡稱': dnz(s.cell_value(i, idx['客戶簡稱'])), '業務': dnz(s.cell_value(i, idx['業務'])),
                     '助理': dnz(s.cell_value(i, idx['助理'])), '品牌': dnz(s.cell_value(i, idx['品牌']))}
    return out


# ══ R-0916-3（Amber 林彥博 2026-09-16 授權·D1⒝·純載入層）T組清冊 glob 擇優 ══
# 硬讀單一檔名在「同一份主檔以不同檔名回傳」時會靜默取到舊版（0912／0915 兩輪實證）。
# 擇優鍵：①表頭命中 ROSTER_COLS 數（新版 68/69 欄與舊版 22 欄皆帶完整表頭，缺表頭者排後）
#         ②候選名稱優先序（新名在前）。判定邏輯一行未動。
ROSTER_CANDIDATES_T = ('T組客戶.XLS', 'T組客戶清冊.XLS')


def _roster_hdr_hits(path):
    """回傳表頭命中 ROSTER_COLS 之欄數；讀不開回 -1（不臆測·排到最後）。"""
    try:
        s_ = xlrd.open_workbook(path).sheet_by_index(0)
        hdr_ = [dnz(s_.cell_value(0, c)) for c in range(s_.ncols)]
    except Exception:
        return -1
    return sum(1 for k in ROSTER_COLS if k in hdr_)


def pick_roster(cands, label='T組'):
    # R-0916-20 修正（留痕層）：候選改為 glob 樣式後，「未採用」須列**實際檔案**而非樣式字串，
    # 否則留痕會把樣式當檔名印出、無法核對。純列印層，擇優鍵與回傳值一行未動。
    best, seen = None, []
    for i, q in enumerate(cands):
        for pth in _glob.glob(q):
            if pth in seen:
                continue
            seen.append(pth)
            hits = _roster_hdr_hits(pth)
            key = (hits, -i)
            if best is None or key > best[0]:
                best = (key, pth, hits)
    if best is None:
        raise FileNotFoundError('%s客戶清冊：候選 %s 全部不存在（R-0916-3／R-0916-20）' % (label, list(cands)))
    _, pth, hits = best
    others = [p for p in seen if p != pth]
    print('  ℹ️ %s清冊採用 %s（表頭命中 %d/%d·R-0916-3／R-0916-20）%s'
          % (label, pth, hits, len(ROSTER_COLS),
             ('｜同時存在但未採用：%s' % others) if others else ''))
    return pth


# ══ R-0916-20（Amber 林彥博 2026-09-16「T1-F 是·納入同一支 v582」·純載入層）T1組清冊 glob 擇優 ══
# 與 R-0916-3 同型同級：0916 回傳之 T1 新清冊檔名為 `T1 客戶清冊.XLS`（69 欄／175 列），
#   與 PROJECT 內既有 `T1組客戶清冊.XLS`（5/23·21 欄／172 列）不同名 → 硬讀舊名會靜默取到舊版
#   （T組已於 0912／0915 兩輪實證同型事故）。
# 併入 R-0916-16b 之教訓：PROJECT 落檔會加「上傳序號前綴」，故樣式兩側皆包 *。
# 擇優鍵：①表頭命中 ROSTER_COLS 數 ②候選順序（新名在前）。全缺則 raise，不靜默 fallback。
ROSTER_CANDIDATES_T1 = ('*T1 客戶清冊*.XLS', '*T1 客戶清冊*.xls',
                        '*T1組客戶清冊*.XLS', '*T1組客戶清冊*.xls')

ROSTER = read_roster(pick_roster(ROSTER_CANDIDATES_T, 'T組'))
ROSTER.update(read_roster(pick_roster(ROSTER_CANDIDATES_T1, 'T1組')))
OVR = _json.load(open('brand_code_overrides_v1_1.json', encoding='utf-8'))
OVR_MAP = {dnz(k).zfill(6): v for k, v in OVR.get('overrides', {}).items()}
# R-0916-4（Amber 林彥博 2026-09-16「C5入白名單」）：7w 抑制白名單（字典驅動·具名逐筆）
SUPPRESS_7W = {dnz(k).zfill(6): v for k, v in OVR.get('suppress_7w', {}).items()}
# ══ R-0916-16（Amber 林彥博 2026-09-16 授權·E5·純載入層）品牌主檔 glob 擇優 ══
# 與 R-0916-3 同型同級：同一份主檔以不同檔名回傳時，硬讀單一檔名會靜默取到舊版。
# 擇優鍵：①表頭命中 BRAND_COLS 數 ②候選順序（新名在前）。全缺則 raise，不靜默 fallback。
BRAND_COLS = ('品牌代碼', '品牌名稱', '主管')
# R-0916-16b：容忍上傳序號前綴（PROJECT 實測會加 `<epoch>_`）與 CSV/TSV 文字副本
BRAND_CANDIDATES = ('*品牌代號清冊*.XLS', '*品牌代號清冊*.xls',
                    '*品牌代號清冊*.csv', '*品牌代號清冊*.tsv',
                    '*brands品牌代碼對照表*.XLS', '*brands品牌代碼對照表*.xls',
                    '*brands品牌代碼對照表*.csv', '*brands品牌代碼對照表*.tsv')


def _brand_rows(path):
    """回傳 [[cell,...],...]；.xls 走 xlrd，.csv/.tsv 走文字（big5/cp950/utf-8 依序嘗試）。"""
    if path.lower().endswith(('.csv', '.tsv')):
        import csv as _csv
        txt = None
        for _enc in ('utf-8-sig', 'utf-8', 'big5', 'cp950'):
            try:
                txt = open(path, encoding=_enc, errors='strict').read()
                break
            except Exception:
                continue
        if txt is None:
            raise ValueError('品牌主檔 CSV 編碼無法判讀：%s' % path)
        _d = '\t' if (path.lower().endswith('.tsv') or '\t' in txt.split('\n')[0]) else ','
        return [[dnz(x) for x in row] for row in _csv.reader(txt.splitlines(), delimiter=_d)]
    s_ = xlrd.open_workbook(path).sheet_by_index(0)
    return [[dnz(s_.cell_value(r, c)) for c in range(s_.ncols)] for r in range(s_.nrows)]


def _brand_hdr_hits(path):
    """回傳表頭命中 BRAND_COLS 之欄數；讀不開回 -1（不臆測·排到最後）。"""
    try:
        hdr_ = _brand_rows(path)[0]
    except Exception:
        return -1
    return sum(1 for k in BRAND_COLS if k in hdr_)


def pick_brands(cands=BRAND_CANDIDATES, label='品牌主檔'):
    best = None
    seen = []
    for i, q in enumerate(cands):
        for pth in sorted(_glob.glob(q)):
            seen.append(pth)
            hits = _brand_hdr_hits(pth)
            key = (hits, -i)
            if best is None or key > best[0]:
                best = (key, pth, hits)
    if best is None:
        raise FileNotFoundError('%s：候選 %s 全部不存在（R-0916-16）' % (label, list(cands)))
    _, pth, hits = best
    others = [q for q in seen if q != pth]
    print('  ℹ️ %s採用 %s（表頭命中 %d/%d·R-0916-16）%s'
          % (label, pth, hits, len(BRAND_COLS),
             ('｜同時存在但未採用：%s' % others) if others else ''))
    return pth


_brows = _brand_rows(pick_brands())
BRANDS = {}
for _r in _brows[1:]:
    _c = dnz(_r[0]) if _r else ''
    if _c:
        BRANDS[_c] = (dnz(_r[1]) if len(_r) > 1 else '', dnz(_r[2]) if len(_r) > 2 else '')


def cust_code(v):
    s = dnz(v)
    if s and re.fullmatch(r'\d+', s):
        s = str(int(s)).zfill(6)
    return s


def enrich(code):
    r = ROSTER.get(code, {})
    bcode = r.get('品牌', '')
    src = '清冊'
    if not bcode and code in OVR_MAP:
        o = OVR_MAP[code]
        bcode = dnz(o.get('brand_code', ''))
        src = '覆蓋表'
    bname, pm = BRANDS.get(bcode, ('', ''))
    if src == '覆蓋表':
        o = OVR_MAP[code]
        bname = dnz(o.get('_ref_brand_name', bname)) or bname
        pm = dnz(o.get('_ref_brand_pm', pm)) or pm
    return r.get('簡稱', ''), r.get('業務', ''), r.get('助理', ''), bcode, bname, pm


# ---------- 4. NT/NS ----------
def _highest_ntns():
    best, bv = None, -1
    for d in ('/home/claude/dpr', '/mnt/project', '.'):
        for p in _glob.glob(d + '/ntns_dict_v*.json'):
            m = re.search(r'_v(\d+)\.json', p)
            if m and int(m.group(1)) > bv:
                bv, best = int(m.group(1)), p
    return best, bv


_ntp, NTNS_VER = _highest_ntns()
_nt = _json.load(open(_ntp, encoding='utf-8'))
NTNS = {k.upper(): v for k, v in _nt['keys'].items() if len(k) >= 5}
# 留白待判清單改由字典 protected.pending_blank 動態讀取（R-v505-2 防禦性 pop·不得臆測）
PENDING_BLANK = set(_nt.get('protected', {}).get('pending_blank', [])) | {'81H55002V'}
for _pb in PENDING_BLANK:
    NTNS.pop(_pb, None)
# R-0819-7（Amber 林彥博 2026-08-19·轉正·永久）：99Z 家族＝特殊品名／加工單號，無可分類屬性
#   amber_ruling：「99Z01/02/03/19都是特殊品名或加工單號，無法一以避之，不得入表」
#   落地：不進 8.NTNS未分類、不寫入 keys；1.主分析 NT/NS 欄標示排除依據。
#   與 R-v496-1（嚴禁前綴推導）不衝突——本規則不賦值，僅宣告「不進分類流程」。
_EXC = (_nt.get('protected', {}).get('excluded_sheet8') or {})
EXC_RE = re.compile(_EXC.get('regex', '^99Z(01|02|03|19)'))
EXC_TXT = '特殊品名/加工單號·不列NT/NS(R-0819-7) / Tên SP đặc biệt hoặc mã gia công, không phân loại NT-NS'
for _k in [k for k in NTNS if EXC_RE.match(k)]:
    NTNS.pop(_k, None)
assert NTNS.get('68QE756VA') == 'NT', 'Amber 0629 特裁防禦失敗'
assert NTNS.get('81TB527VM') == 'NS', 'R-v504-4 具名裁決防禦失敗'
assert NTNS.get('68QE523VA') == 'NT', 'R-v518-1 防禦失敗'
PENDING_MATS = PENDING_BLANK
print(f"NT/NS v{NTNS_VER} 鍵數={len(NTNS)}（R-v523-1 採認態·counts={_nt['counts']}·留白待判 {sorted(PENDING_BLANK)}）")


def ntns_of(mat):
    return NTNS.get(dnz(mat).upper(), '')


# ---------- 5. 回填字典 ----------
def _highest_columnar():
    best, bv = None, -1
    for d in ('/home/claude/dpr', '/mnt/project', '.'):
        # R-0903-1（Amber 林彥博 2026-09-03「A1-b」·轉正·永久）：字典改以 .json.gz 落回 PROJECT FILES
        #   （json 1.41MB 超出 PROJECT 可用空間；gz9 約 105KB·load_any 原生支援 .gz）→ glob 須同步接受。
        for p in (_glob.glob(d + '/回填原因處置字典_v*_columnar.json')
                  + _glob.glob(d + '/回填原因處置字典_v*_columnar.json.gz')):
            m = re.search(r'_v(\d+)_columnar', p)
            if m and int(m.group(1)) > bv:
                bv, best = int(m.group(1)), p
    return best, bv


_dcp, DICT_VER = _highest_columnar()
D = load_any(_dcp)
RULE_5141 = D.get('rule_R_v514_1') or {}
assert 'Amber' in RULE_5141.get('ruled_by', ''), 'rule_R_v514_1 缺失或未具名'
EXEMPT_RE = re.compile((D.get('rule_R_v506_1') or {}).get('exempt_regex', '客戶預告新增數量|KH TĂNG SL DỰ BÁO'))
R252 = D.get('rule_R_v525_2') or {}
assert 'Amber' in str(R252.get('ruled_by', '')), 'rule_R_v525_2 缺失或未具名（v24 契約）'
RX252 = re.compile(R252['regex'])
AGE_LIM = int(R252.get('age_threshold_days', 90))
ORDERS = D['orders']
CAP_SET = {dnz(it.get('order')) for it in D['cap_locked_0702'].get('items', [])}
CAP_SET |= {k for k, v in ORDERS.items() if dnz(v.get('cap_reached')) == '🛑'}
_pck = max((k for k in D if re.match(r'phrase_classifier_v\d+$', k)), key=lambda k: int(k.rsplit('v', 1)[1]))
PC_MAP = dict(D[_pck]['map'])
N_ARJ = sum(1 for _v in ORDERS.values() if _v.get('answer_rejected'))
# ══ R-0908-4（Amber 林彥博 2026-09-08·具名裁決）結案後復檢·個案豁免 ══
# amber_ruling：於 0908 回傳檔 6b「處理方式和結果」欄逐列填寫「合理回報，請結案不要再複查」。
# 語意：Amber 已逐單審閱該批 89 之回填內容並認定合理 → ⒜結案 ⒝停止 R-0819-1 之♻️復檢回列。
# 範圍界定（R-0819-2 不泛化）：**僅豁免字典 no_recheck_orders 逐一具名之單號**；
#   R-0819-1 規則本身（轉正·永久）一字未動，未具名之結案未消耗 89 仍一律回列復檢。
# 落點：6b 群組迴圈中，具名者不標♻️、不留在 6b，改推入 9.已結案移除（互斥鐵則 A2 因此仍成立）。
NO_RECHECK = {dnz(_o).upper() for _o in (D.get('rule_R_0908_4') or {}).get('no_recheck_orders', [])}
print(f"字典 v{DICT_VER}：orders={len(ORDERS)} cap集合={len(CAP_SET)} phrase鍵={len(PC_MAP)}（classifier {_pck.rsplit('_',1)[-1]}）·answer_rejected={N_ARJ}"
      f"·R-0908-4 復檢豁免={len(NO_RECHECK)} 單")

# ---------- 6. 逐列分類 ----------
RE_KN = re.compile(r'KNKH|KN\d|[-/]KN|KN$')
RE_LL = re.compile(r'^LL|[-/]LL|LL$')
RE_XLBT = re.compile(r'XLBT')
HIGH = '🔴 高風險 / Rủi ro cao HIGH'
MEDH = '🟠 中高風險 / Rủi ro trung-cao MED-HIGH'
MED = '🟡 中風險 / Rủi ro trung bình MEDIUM'
LOW = '⚪ 低風險 / Rủi ro thấp LOW'
OKR = 'OK / Bình thường'
LV89 = '—89預告不列異常(R-v522-2) / DB 89 không tính bất thường tiến độ'

ANA = []
for r in active:
    cat = dnz(r[0])
    code = cust_code(r[1])
    order = dnz(r[2]).upper()
    is89 = (cat == '89')
    prod = math.floor(fnum(r[34]))
    sample = cat in ('85', '86', '87')
    massp = cat == '88'
    sq19_empty = fnum(r[6]) == 0
    grace = (prod <= 2) and sq19_empty and not is89
    okh_raw = r[38]
    over_kh = None
    f = fnum(okh_raw)
    if dnz(okh_raw) not in ('', '-'):
        if f > ERP_DEGENERATE_MIN:
            d = as_date(okh_raw)
            if d:
                dd = (TODAY - d).days
                over_kh = dd if dd > 0 else None
        elif f > 0:
            over_kh = math.floor(f)
    _st36, over_std = erp_days(r[36])
    _st37, _d37 = erp_days(r[37])
    o19 = _d37 or 0
    o19_status, o19_note = None, ''
    if _st37 == 'over' and o19 > 0:
        h = as_date(r[7])
        if h is None:
            o19_status = 'delay'
            o19_note = f'過1.9交期{math.floor(o19)}天，生管無Mail更新 / Quá 1.9 {math.floor(o19)} ngày, SQ chưa cập nhật mail'
        elif TODAY > h:
            o19_status = 'delay'
            o19_note = f'過1.9交期，Mail更新交期亦已逾期{(TODAY-h).days}天 / Mail cập nhật cũng đã quá {(TODAY-h).days} ngày'
        else:
            o19_status = 'not_delay'
            o19_note = f'過1.9交期，Mail更新交期尚餘{(h-TODAY).days}天 / Còn {(h-TODAY).days} ngày theo mail'
    test = dnz(r[32]).upper()
    yarn = dnz(r[10]) == '✔'
    upd = dnz(r[19])
    no_update = upd.startswith('否')
    prog_same = dnz(r[17]) == dnz(r[18]) and dnz(r[18]) != ''
    reply_blank = fnum(r[5]) == 0 and not is89
    bl_ok = dnz(r[39]) == '✔'
    prio = (not is89) and bool(RE_KN.search(order) or RE_LL.search(order) or RE_XLBT.search(order))
    major = (not is89) and yarn and no_update and prog_same
    reasons = []
    level = 'OK'
    if is89:
        level = LV89
        reasons.append('89預告·進度異常不適用(R-v522-2)·異常管理走 4b/6/6b/觀察 / DB 89: quản lý qua 4b/6/6b/theo dõi')
    else:
        delay = ((sample and prod >= 14) or (massp and prod >= 30) or o19_status == 'delay'
                 or (over_kh is not None) or test == 'F')
        warn = ((sample and prod >= 10) or (massp and prod >= 21) or (over_std is not None)
                or o19_status == 'not_delay' or test == 'Q' or yarn or bl_ok)
        pot = ((prog_same and no_update) or no_update or reply_blank or test in ('T', '0', 'B'))
        if grace and not (prio or major):
            level = 'OK'
            reasons.append('下單≤2天，待生管回覆1.9 / Đơn ≤2 ngày, chờ SQ phản hồi 1.9')
        elif delay:
            level = 'DELAY'
        elif warn:
            level = 'WARNING'
        elif pot:
            level = 'POTENTIAL'
        if prio or major:
            level = 'DELAY'
        if level != 'OK' or prio or major:
            if yarn:
                reasons.append('缺紗 / Thiếu sợi')
            if prog_same and no_update:
                reasons.append('進度連續停滯 / Tiến độ đình trệ liên tục')
            elif no_update:
                reasons.append('潛在停滯待確認 / Có thể đình trệ, cần xác nhận')
            if over_kh is not None:
                reasons.append(f'過客戶交期{over_kh}天 / Quá {over_kh} ngày giao KH')
            if o19_note:
                reasons.append(o19_note)
            if over_std is not None and level != 'DELAY':
                reasons.append(f'過標準交期{over_std}天 / Quá {over_std} ngày giao TC')
            tmap = {'F': '測試FAIL / Kết quả KT: Fail', 'Q': '特採出貨 / Xuất đặc chuẩn',
                    'T': '測試中 / Đang kiểm tra', '0': '無測試報告 / Chưa có BC KT',
                    'B': '測試後補 / Bổ sung sau KT'}
            if test in tmap:
                reasons.append(tmap[test])
            if bl_ok:
                reasons.append('⚠️保留需確認是否成品 / Cần XN tồn kho TP')
            if reply_blank:
                reasons.append('未回覆客戶 / Chưa trả lời KH')
            if sample and prod >= 14:
                reasons.append(f'樣品生產{prod}天(≥14) / Mẫu SX {prod} ngày')
            elif massp and prod >= 30:
                reasons.append(f'量產生產{prod}天(≥30) / SX {prod} ngày')
            elif sample and prod >= 10:
                reasons.append(f'樣品生產{prod}天(≥10) / Mẫu SX {prod} ngày')
            elif massp and prod >= 21:
                reasons.append(f'量產生產{prod}天(≥21) / SX {prod} ngày')
        if prio:
            tag = 'KN客訴' if RE_KN.search(order) else ('LL重做' if RE_LL.search(order) else 'XLBT異常處理')
            reasons.insert(0, f'⭐最優先({tag})·3-5天 / Ưu tiên cao nhất')
        if major:
            reasons.insert(0, '🆘重大異常(缺紗+停滯)·立即升級採購排料 / Khẩn cấp: thiếu sợi + đình trệ')
    if is89:
        risk = '— / DB 89'
    elif prio or major:
        risk = HIGH
    elif level == 'DELAY':
        risk = HIGH if (over_kh is not None or yarn or test == 'F') else MEDH
    elif level == 'WARNING':
        risk = MEDH if yarn else MED
    elif level == 'POTENTIAL':
        risk = LOW
    else:
        risk = OKR
    disp = []
    rtxt = '；'.join(reasons)
    if not is89:
        if '缺紗' in rtxt:
            disp.append('確認採購到料日，評估替代料，告知客戶 / XN ngày nhận NVL, đánh giá thay thế, báo KH')
        if '停滯' in rtxt:
            disp.append('助理聯繫生管確認並更新進度 / Trợ lý liên hệ SQ XN & cập nhật tiến độ')
        if '過客戶交期' in rtxt:
            disp.append('業務立即回覆客戶提供新完工日 / NV trả lời KH ngay, cung cấp ngày HT mới')
        if '測試FAIL' in rtxt:
            disp.append('工程評估補測/改善方案 / KT đánh giá bổ sung/cải thiện')
        if '特採' in rtxt:
            disp.append('確認特採核准並保留紀錄 / XN phê duyệt đặc chuẩn & lưu hồ sơ')
        if '保留需確認' in rtxt:
            disp.append('助理確認保留是否成品 / Trợ lý XN tồn kho có phải TP không')
        if 'Mail更新' in rtxt:
            disp.append('確認Mail更新交期是否已告知客戶 / XN đã báo KH ngày giao mới qua mail chưa')
        if '未回覆客戶' in rtxt:
            disp.append('助理補填回復客戶日期 / Trợ lý bổ sung ngày TL KH')
        if not disp:
            if level == 'DELAY':
                disp.append('業務主動告知客戶延期 / NV chủ động báo KH về trễ hàng')
            elif level == 'WARNING':
                disp.append('助理每日追蹤 / Trợ lý theo dõi hàng ngày')
            elif level == 'OK' and grace:
                disp.append('待生管回覆1.9後重新判定 / Chờ SQ phản hồi 1.9 rồi đánh giá lại')
    sc, nv_r, tl_r, bc, bn, pm = enrich(code)
    tl_src = dnz(r[43]) if NCOLS >= 44 else ''
    nv_src = dnz(r[44]) if NCOLS == 45 else ''
    nv_val = nv_bi(nv_src or nv_r) if (nv_src or nv_r) else ('—(T1無業務欄) / (T1 không có cột NV)' if IS_T1 else '')
    tl_val = nv_bi(tl_src or tl_r)
    ANA.append({'row': r, 'cat': cat, 'code': code, 'order': order, 'is89': is89,
                'level': level, 'risk': risk, 'reasons': rtxt, 'disp': '；'.join(disp),
                'ntns': ntns_of(r[11]), 'sc': sc, 'nv': nv_val, 'tl': tl_val,
                'bc': bc, 'bn': bn, 'pm': pm, 'prio': prio, 'major': major,
                'yarn': yarn, 'no_update': no_update, 'prog_same': prog_same,
                'otd': otd_of(r, as_date(r[4])),
                'has_dc': dnz(r[30]) not in ('', '0'),
                'kept': fnum(r[23]) > 0,
                'mat': dnz(r[11]).upper(), 'pname': dnz(r[26]) or dnz(r[25]),
                'undel': undel(r), 'unit': dnz(r[16])})

from collections import Counter
C = Counter(a['level'] for a in ANA if not a['is89'])
_89dates = [as_date(a['row'][4]) for a in ANA if a['is89']]
# ══ R-0916-35（Amber 林彥博 2026-09-16「H1-是，但只限於資料抓取的時間範圍，且未包含跨組別的預告資料」）══
# 89DB 累積檔：①依組別擇檔 ②讀 `_scope` 分頁驗證組別與期間 ③組別不符一律不採（視同缺檔）。
# 立論：覆蓋率閘門只看日期、不看組別 —— 若把 T1 的累積檔拿去算 T組，會**錯誤地**判為已覆蓋。
import os as _os
import openpyxl as _openpyxl
ACC_CANDS = ('89DB_累積_%s.xlsx' % GROUP, '89DB_累積.xlsx')
ACC_PATH, ACC_SCOPE, ACC_NOTE = None, {}, ''
for _c in ACC_CANDS:
    for _d in ('/home/claude/dpr', '/mnt/project', '/mnt/user-data/outputs', '.'):
        _p = _d + '/' + _c
        if not _os.path.exists(_p):
            continue
        try:
            _wbA = _openpyxl.load_workbook(_p, read_only=True, data_only=True)
            _sc = {}
            if '_scope' in _wbA.sheetnames:
                for _rw in _wbA['_scope'].iter_rows(min_row=2, values_only=True):
                    if _rw and _rw[0]:
                        _sc[dnz(_rw[0])] = dnz(_rw[1]) if len(_rw) > 1 else ''
        except Exception as _e:
            ACC_NOTE = '累積檔 %s 讀取失敗（%s）→ 不採用' % (_c, type(_e).__name__)
            continue
        _g = _sc.get('group', '')
        if _g and _g != GROUP:
            ACC_NOTE = '累積檔 %s 之 _scope.group=%s ≠ 本輪 %s → **不採用**（R-0916-35 禁跨組別共用）' % (_c, _g, GROUP)
            continue
        ACC_PATH, ACC_SCOPE = _p, _sc
        ACC_NOTE = ('採用 %s｜組別 %s｜抓取期間 %s ~ %s｜%s 列（R-0916-35）'
                    % (_c, _g or '(未宣告)', _sc.get('range_start', '?'), _sc.get('range_end', '?'),
                       _sc.get('rows', '?')))
        break
    if ACC_PATH:
        break
# ══ R-0918-9（Amber 林彥博 2026-09-18「沒收到檔案的話就每輪重建」·轉正）══
# 未收到累積檔 → 以本輪追蹤表未完成 89（R-0917-25 同法）重建 `89DB_累積_<組>.xlsx`，落工作目錄＋outputs。
# ★界線（R-0917-25 已留痕）：自追蹤表重建者覆蓋率在算式上必然 100%，只代表 active 89 母體；
#   不含已結案 89、不含實秤欄 → R-0918-8 跨計量類別換算於此情形不可用（一律待裁決）。
if not ACC_PATH and GROUP in ('T組', 'T1組'):
    _prev_note = ACC_NOTE
    _rb = [x for x in ANA if x['is89']]
    _wbR = _openpyxl.Workbook()
    _wsR = _wbR.active
    _wsR.title = '89DB'
    _wsR.append(['89單號', '序號', '首見日', '客戶代碼', '料號', '色號', '寬度', '型號', '單位',
                 '數量', '完工量', '已交量', '未交量'])
    _ds = []
    for _x in _rb:
        _r = _x['row']
        _d = as_date(_r[4])
        _ds.append(_d)
        _wsR.append([_x['order'], dnz(_r[3]), _d.isoformat() if _d else '', _x['code'], dnz(_r[11]), dnz(_r[12]),
                     fnum(_r[13]), dnz(_r[14]), dnz(_r[16]), fnum(_r[15]), fnum(_r[20]), fnum(_r[21]), undel(_r)])
    _ds = [d for d in _ds if d]
    _scR = {'group': GROUP, 'range_start': min(_ds).isoformat() if _ds else '',
            'range_end': max(_ds).isoformat() if _ds else '', 'rows': str(len(_rb)),
            'source': 'R-0918-9 自追蹤表未完成89重建（%s）·未收到累積檔' % INPUT}
    _wsS = _wbR.create_sheet('_scope')
    _wsS.append(['key', 'value'])
    for _kk, _vv in _scR.items():
        _wsS.append([_kk, _vv])
    _wsR.freeze_panes = None
    _pR = '/home/claude/dpr/' + ACC_CANDS[0] if _os.path.isdir('/home/claude/dpr') else ACC_CANDS[0]
    _wbR.save(_pR)
    try:
        if _os.path.isdir('/mnt/user-data/outputs'):
            _wbR.save('/mnt/user-data/outputs/' + ACC_CANDS[0])
    except Exception:
        pass
    ACC_PATH, ACC_SCOPE = _pR, _scR
    ACC_NOTE = ('R-0918-9 重建 %s｜組別 %s｜期間 %s ~ %s｜%s 列｜來源＝本輪追蹤表未完成89（前狀態：%s）'
                % (ACC_CANDS[0], GROUP, _scR['range_start'], _scR['range_end'], _scR['rows'],
                   _prev_note or '未提供'))
if not ACC_PATH:
    ACC_NOTE = ACC_NOTE or '89DB 累積檔未提供（候選 %s）' % list(ACC_CANDS)
# R-0918-8：由累積檔實秤欄建立每單位實秤淨重（同 料號/寬度/型號）；欄缺則不建（跨類別換算一律待裁決）
if ACC_PATH:
    try:
        _wsW = _openpyxl.load_workbook(ACC_PATH, read_only=True, data_only=True).worksheets[0]
        _it = _wsW.iter_rows(values_only=True)
        _hW = [dnz(c) for c in next(_it)]
        if all(k in _hW for k in ('實秤淨重(KG)', '實秤數量', '單位', '料號', '寬度', '型號')):
            _iw, _in, _iu = _hW.index('實秤淨重(KG)'), _hW.index('實秤數量'), _hW.index('單位')
            _im, _iwd, _imd = _hW.index('料號'), _hW.index('寬度'), _hW.index('型號')
            from collections import defaultdict as _dd; _agg = _dd(lambda: [0.0, 0.0])
            for _rw in _it:
                _w, _n = fnum(_rw[_iw]), fnum(_rw[_in])
                if _w > 0 and _n > 0:
                    _kk = ((dnz(_rw[_im]).upper(), fnum(_rw[_iwd]), dnz(_rw[_imd]).upper()), dnz(_rw[_iu]).upper())
                    _agg[_kk][0] += _w
                    _agg[_kk][1] += _n
            for (_sp, _uu), (_w, _n) in _agg.items():
                WT_KGPU.setdefault(_sp, {})[_uu] = _w / _n
    except Exception as _e:
        print('  ⚠️ R-0918-8 實秤表建立失敗（%s）→ 跨類別換算一律待裁決' % type(_e).__name__)
print('  ℹ️ R-0918-8 實秤換算表：%d 規格' % len(WT_KGPU))
print('  ℹ️ 89DB 累積檔：%s' % ACC_NOTE)
COV = lc.sheet4_coverage_gate(_89dates, accum_path=(ACC_PATH.split('/')[-1] if ACC_PATH else '__absent__.xlsx'))
SHEET4_GATE = COV['gate_met'] or PRE['interval_89_files'] >= 12
# R-0916-35 守門：採用了累積檔、起始日卻仍是程式預設 → 幾乎必然是表頭讀不到（hdr.index('首見日') 精確比對）。
#   這種失敗原本被 lc 的 except 吞掉、完全看不出來 —— 明示警告，不讓它靜默。
if ACC_PATH and COV['start'] == '2026-07-08':
    print('  ⚠️ 累積檔已採用但起始日仍為程式預設 2026-07-08 → 請檢查該檔首張工作表是否有**單語精確表頭「首見日」**'
          '（雙語表頭會讀不到·R-0916-35）')
print('R-v527-1 覆蓋:', COV, '| SHEET4_GATE =', SHEET4_GATE)
print('等級(排除89):', dict(C), '| ⭐優先=%d 🆘重大=%d' % (sum(a['prio'] for a in ANA), sum(a['major'] for a in ANA)))
with open('_stage_part1.pkl', 'wb') as f:
    pickle.dump({'ANA_len': len(ANA)}, f)
print('PART1 OK')

# ==================== PART 2 ====================
from collections import defaultdict


def order_days(r):
    d = as_date(r[4])
    return (TODAY - d).days if d else None


LOCK_TXT = ('🔒鎖定(cap🛑·R-v492-1)·強制業務處置·限期三選一(①XSD刪單②轉組③採購凍結)'
            '·禁第三次回歸觀察·不得等後單 / Khóa cap: NV bắt buộc xử lý, chọn 1 trong 3'
            '(①XSD ②chuyển tổ ③đóng băng mua), không chờ đơn sau')
FORCE_TXT = ('⛔FORCE·死預告(KHÔNG CÒN ĐƠN SD)·限期三選一(①XSD刪單②轉組③採購凍結)'
             ' / DB chết, chọn 1 trong 3(①XSD ②chuyển tổ ③đóng băng mua)')
FORCE_252_TXT = ('⛔FORCE·現無單使用且帳齡>90天(R-v525-2)·限期三選一(①XSD刪單②轉組③採購凍結)·不入觀察'
                 ' / Hiện không có đơn dùng & tuổi >90 ngày: chọn 1 trong 3, không theo dõi')


def _norm_raw(s):
    s = re.sub(r'\s+', ' ', (s or '').strip()).upper()
    return re.sub(r'\s*,\s*', ',', s)


def eff_window(rec):
    cands = [dnz(rec.get('monitor_until')), dnz((rec.get('claim_verify') or {}).get('monitor_until'))]
    bd = dnz(rec.get('backfill_date'))
    if bd:
        try:
            cands.append((datetime.date.fromisoformat(bd[:10]) + datetime.timedelta(days=15)).isoformat())
        except ValueError:
            pass
    cands = [x for x in cands if x]
    return max(cands) if cands else ''


def resolved_state(o):
    rec = ORDERS.get(o)
    if not rec:
        return None, ''
    st = dnz(rec.get('status'))
    if rec.get('answer_rejected'):
        return None, ''
    if st in ('CLOSED', 'PROCESSED'):
        return 'CLOSED', ''
    hit = PC_MAP.get(_norm_raw(dnz(rec.get('raw_reason'))))
    if hit and hit.get('status') == 'CLOSED':
        return 'CLOSED', ''
    if st == 'PROCESSING':
        return 'PROCESSING', ''
    ew = eff_window(rec)
    if st == 'OPEN' and ew and ew >= TODAY.isoformat():
        return 'WINDOW', ew
    return None, ew


S6, S6W, S6B_SRC, S9 = [], [], [], []
cand6 = [a for a in ANA if a['is89'] and fnum(a['row'][21]) == 0 and fnum(a['row'][23]) == 0]
for a in cand6:
    r = a['row']
    o = a['order']
    rec = ORDERS.get(o) or ORDERS.get(dnz(r[2]))
    days = order_days(r)
    incap = o in CAP_SET
    old_reason = ''
    old_date = ''
    refill = 0
    if rec:
        old_reason = dnz(rec.get('raw_reason'))
        old_date = dnz(rec.get('backfill_date'))
        refill = len(rec.get('backfill_history') or []) or (1 if old_reason else 0)
    st = dnz(rec.get('status')) if rec else ''
    rawU = _norm_raw(old_reason)
    is_252 = bool(RX252.search(rawU)) and 'KHÔNG CÒN' not in rawU and 'KHONG CON' not in rawU
    if st in ('CLOSED', 'PROCESSED'):
        S9.append((a, '6', st, old_reason, old_date))
        continue
    if st == 'FORCE':
        ftxt = FORCE_252_TXT if is_252 else FORCE_TXT
        if incap and is_252:
            ftxt += '｜雙依據：R-v525-2 帳齡＋R-v497-2 cap🛑禁三進'
        _arj = bool(rec.get('answer_rejected'))
        if _arj:
            ftxt = ('❌回答被駁回(R-v539-1)·「đang chờ đơn mới」答非所問不受理·cap🛑不解鎖·恆追問三選一至具體選擇'
                    ' / Câu trả lời bị bác (R-v539-1)'
                    '｜📌' + dnz(rec.get('directive')) + '｜') + ftxt
        if rec.get('conflict_flag'):
            ftxt = '⚔️跨表衝突登錄·FORCE 待Amber終裁(R-v539-3)·' + ftxt
        S6.append(dict(a, life='⛔FORCE', arj=_arj, prog=ftxt, old=old_reason, old_d=old_date, days=days, refill=refill))
        continue
    if st == 'PROCESSING':
        S6.append(dict(a, life='🔧處理中', prog='🔧處理中·待結果 / Đang xử lý, chờ kết quả',
                       old=old_reason, old_d=old_date, days=days, refill=refill))
        continue
    if st == 'OPEN':
        if rec.get('directive'):
            _arj = bool(rec.get('answer_rejected'))
            _pfx = ('❌回答被駁回·重問(R-v539)·不適用信任窗·'
                    ' / Câu trả lời bị bác — vui lòng trả lời lại·') if _arj else ''
            S6.append(dict(a, life=('❌駁回重問' if _arj else '📌主管提問'), arj=_arj,
                           days=days, refill=refill, old=old_reason, old_d=old_date,
                           prog=_pfx + (f"📌主管提問(R-v529-2)·原文：{dnz(rec.get('directive'))}·請業務/助理於反黃兩欄作答"
                                 f" / Câu hỏi của quản lý: {dnz(rec.get('directive'))} —"
                                 f" vui lòng NV/trợ lý trả lời vào 2 cột vàng")))
            continue
        pc_hit = PC_MAP.get(rawU)
        if pc_hit and pc_hit.get('status') == 'CLOSED':
            S9.append((a, '6', 'CLOSED(語句)', old_reason, old_date))
            continue
        if 'KHÔNG CÒN ĐƠN' in rawU or 'KHONG CON DON' in rawU:
            S6.append(dict(a, life='⛔FORCE', prog=FORCE_TXT, old=old_reason, old_d=old_date,
                           days=days, refill=refill))
            continue
        if is_252 and (days or 0) > AGE_LIM:
            ftxt = FORCE_252_TXT + ('｜雙依據：R-v525-2 帳齡＋R-v497-2 cap🛑禁三進' if incap else '')
            S6.append(dict(a, life='⛔FORCE', prog=ftxt, old=old_reason, old_d=old_date,
                           days=days, refill=refill))
            continue
        mu = eff_window(rec) or dnz(rec.get('monitor_until'))
        _cv = (rec.get('claim_verify') or {})
        _ar = _cv.get('amber_ruling', '')
        _combo = ('R-v510-1' in _ar and '不適用' not in _ar)
        if rec.get('pending_use'):
            _mu14 = dnz(_cv.get('monitor_until')) or mu
            S6W.append(dict(a, over='👁暫入觀察·待後單(R-v514-1)' + (f'(至{_mu14})' if _mu14 else ''),
                            prog=('👁暫入觀察·待後單使用(R-v514-1)·有後單掛用/消耗→結案 / '
                                  'Tạm theo dõi chờ đơn sau: có đơn sau gắn dùng/tiêu thụ → đóng'),
                            old=old_reason, old_d=old_date, mu=_mu14, refill=refill, cap=''))
            continue
        if _combo:
            _mu = dnz(_cv.get('monitor_until')) or mu or WAVE_DATE
            _prog = (f'👁R-v510-1組合觀察·有單→結案；到期{_mu}(建議值)無單→移轉/報廢 二選一 / '
                     f'Theo dõi: có đơn → đóng; đến {_mu} không có đơn → chuyển nhóm HOẶC hủy bỏ')
            S6W.append(dict(a, over=f'監控中(至{_mu}·R-v510-1)', prog=_prog,
                            old=old_reason, old_d=old_date, mu=_mu, refill=refill, cap=''))
        elif incap:
            S6W.append(dict(a, over='🔒已鎖定(禁三進)', prog=LOCK_TXT, old=old_reason,
                            old_d=old_date, mu=mu, refill=refill, cap='🛑'))
        elif mu and mu >= TODAY.isoformat():
            S6W.append(dict(a, over=f'監控中(至{mu})',
                            prog=(f'👁觀察窗內·期內不重複詢問(R-v529-1/R-v532-1)·到期{mu}複查 / '
                                  f'Trong thời gian theo dõi (đến {mu}), không hỏi lại'),
                            old=old_reason, old_d=old_date, mu=mu, refill=refill, cap=''))
        else:
            S6.append(dict(a, life='⚠️逾期回歸', days=days, refill=refill, old=old_reason, old_d=old_date,
                           prog=f'⚠️逾期回歸(監控至{mu or "-"}已過)·需重新回填 / Quá hạn theo dõi, cần báo cáo lại'))
        continue
    if incap:
        S6W.append(dict(a, over='🔒已鎖定(禁三進)', prog=LOCK_TXT, old=old_reason, old_d=old_date,
                        mu='', refill=max(refill, 2), cap='🛑'))
        continue
    if days is not None and days >= 31:
        grade = '🔴A·損失>45天' if days > 45 else '🟠B·預警31-45天'
        S6.append(dict(a, life=f'🆕新{grade[1]}', grade=grade, days=days, refill=0, old='', old_d='',
                       prog='🆕新列·請回填原因與處置 / Mới, vui lòng báo cáo nguyên nhân & xử lý'))
for a2 in S6:
    if 'grade' not in a2:
        d = a2.get('days')
        a2['grade'] = ('🔴A·損失>45天' if (d or 0) > 45 else ('🟠B·預警31-45天' if (d or 0) >= 31 else '—'))

# ---- R-0820-1（Amber 林彥博 2026-08-20「落回」→ 2026-08-26「A2-轉正」·轉正·永久）觀察到期自動落回 6 表 ----
# 立意：0819→0820 之 ⏰到期潮 44 單到期分佈完全相同、一日之內零處置。
#   舊行為＝到期者仍留在 6觀察名單、僅加 ⏰ 前綴＋派工「預警」→ 無人處置即無限期停留。
# amber_ruling：「裁-B, 落回」（2026-08-20 立）／「A2-轉正」（2026-08-26 轉正·永久）
# 落地：monitor_until 已過（mu < TODAY）且非 cap🛑 者，自 6觀察名單**移出**、落回
#   6.預告未保留使用 回填表（life='⏰到期回歸'），並改列派工「強制」（限期 DUE_FORCE）。
#   cap🛑 者不受影響（本即走 R-v492-1 強制三選一通道，不得二次降級）。
#   mu == 明日者維持 ⏰ 預警（尚未到期，仍給一日預先處置窗）。
_TODAY_ISO = TODAY.isoformat()
S6W_FALLBACK = [x for x in S6W
                if (not x['cap']) and dnz(x.get('mu')) and dnz(x.get('mu')) < _TODAY_ISO]
_FB_KEYS = {id(x) for x in S6W_FALLBACK}
S6W = [x for x in S6W if id(x) not in _FB_KEYS]
n_fallback = len(S6W_FALLBACK)
for x in S6W_FALLBACK:
    _mu = dnz(x.get('mu'))
    try:
        _late = (TODAY - datetime.date.fromisoformat(_mu[:10])).days
    except ValueError:
        _late = None
    x['life'] = '⏰到期回歸'
    x['days'] = order_days(x['row'])
    x['prog'] = (f'⏰觀察到期自動回歸(R-0820-1·Amber 0820「落回」)·監控至 {_mu} 已過'
                 + (f'{_late} 天' if _late is not None else '')
                 + '·不再留於觀察名單·請即回填處置：有後單掛用/消耗證據→結案；無單→移轉或報廢二選一 / '
                 f'Hết hạn theo dõi ({_mu}) tự động quay lại bảng báo cáo: có đơn sau gắn dùng/tiêu thụ → đóng; '
                 'không có đơn → chuyển tổ HOẶC hủy bỏ')
    S6.append(x)
for a2 in S6:
    if 'grade' not in a2:
        d = a2.get('days')
        a2['grade'] = ('🔴A·損失>45天' if (d or 0) > 45 else ('🟠B·預警31-45天' if (d or 0) >= 31 else '—'))
if n_fallback:
    print(f'R-0820-1 觀察到期落回 6 表：{n_fallback} 單（自 6觀察名單移出·改列派工「強制」）')

n_wave = 0
for x in S6W:
    if not x['cap'] and dnz(x.get('mu')) and dnz(x.get('mu')) <= WAVE_DATE:
        x['over'] = f'⏰即將到期({WAVE_MMDD}潮)·' + x['over']
        x['wave'] = True
        n_wave += 1
    else:
        x['wave'] = False

print(f'Sheet6={len(S6)}（逾期回歸={sum(1 for x in S6 if "逾期" in x["life"])} FORCE={sum(1 for x in S6 if "FORCE" in x["life"])} '
      f'處理中={sum(1 for x in S6 if "處理中" in x["life"])} 新={sum(1 for x in S6 if "新" in x["life"])}）'
      f' 6觀察={len(S6W)}（cap🛑={sum(1 for x in S6W if x["cap"])} 監控={sum(1 for x in S6W if not x["cap"])} ⏰{WAVE_MMDD}潮={n_wave}）')

# ---------- 4b 前置：庫存 ----------
SEMI2FIN = {'31': '39', '33': '66', '37': '77', '41': '61', '45': '65', '47': '67', '48': '68'}
PAIRS = set()
for aa, bb in SEMI2FIN.items():
    PAIRS.add((aa, bb))
    PAIRS.add((bb, aa))
PAIRS.add(('81', '48'))
PAIRS.add(('48', '81'))


def mat_compatible(om, im):
    om, im = om.upper(), im.upper()
    if om == im:
        return True
    if len(om) > 2 and len(im) > 2 and om[2:] == im[2:] and (om[:2], im[:2]) in PAIRS:
        return True
    return False


_INV_ALIAS = {
    'mat':   ('料品代碼', '料號', '產品代號', '品號'),
    'color': ('色號',),
    'w':     ('寬度',),
    'model': ('型號(上漿)', '型號(上滾)', '型號'),
    'unit':  ('單位',),
    'indate': ('入庫日',),
    'slot':  ('格位號', '格位'),
    'qty':   ('數量',),
    'kept':  ('保留量',),
}


def _inv_pick(hdr):
    idx = {}
    norm = [dnz(h).replace(' ', '') for h in hdr]
    for key, names in _INV_ALIAS.items():
        for nm in names:
            if nm in norm:
                idx[key] = norm.index(nm)
                break
    missing = [k for k in _INV_ALIAS if k not in idx]
    assert not missing, f'R-v545-2 庫存表頭缺欄 {missing}｜實際表頭={norm}'
    return idx


def _pdate(s_):
    s_ = dnz(s_)
    m = re.match(r'(\d{1,2})/(\d{1,2})/(\d{4})', s_)
    if m:
        return datetime.date(int(m.group(3)), int(m.group(1)), int(m.group(2)))
    m = re.match(r'(\d{4})-(\d{1,2})-(\d{1,2})', s_)
    if m:
        return datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    f = fnum(s_)
    if f > 20000:
        return EPOCH + datetime.timedelta(days=int(f))
    return None


_inv_cands = []
for _d in ('/home/claude/dpr', '/mnt/project', '/mnt/user-data/uploads', '.'):
    for _pat in ('DB_*.xls', 'DB_*.xlsx', 'DB_*.csv', 'DB_*.XLS', 'DB_*.XLSX', 'DB_*.CSV'):
        for _p in _glob.glob(_d + '/' + _pat):
            if '累積' in _p:
                continue
            _ms = re.findall(r'(\d+)', _p.split('/')[-1])
            _inv_cands.append((tuple(int(x) for x in _ms), _p))
_inv_cands.sort()
INV_PATH = _inv_cands[-1][1] if _inv_cands else None
INV_ABSENT = INV_PATH is None
INV_NAME = INV_PATH.split('/')[-1] if INV_PATH else '（未提供）'
INV_TRUNC = False
INV_NROWS = 0
_inv_raw = []
if not INV_ABSENT:
    if INV_PATH.lower().endswith('.csv'):
        import csv as _csv
        _txt = None
        for _enc in ('big5', 'cp950', 'utf-8-sig', 'utf-8'):
            try:
                _txt = open(INV_PATH, encoding=_enc, errors='strict').read()
                INV_ENC = _enc
                break
            except Exception:
                continue
        assert _txt is not None, f'R-v545-2 庫存 CSV 編碼無法判讀：{INV_NAME}'
        _rd = list(_csv.reader(_txt.splitlines()))
        _hdr = _rd[0]
        _ix = _inv_pick(_hdr)
        for _r in _rd[1:]:
            if len(_r) <= max(_ix.values()):
                continue
            _inv_raw.append({k: _r[i] for k, i in _ix.items()})
        INV_NROWS = len(_inv_raw)
    else:
        INV_ENC = 'xls'
        _wbi = xlrd.open_workbook(INV_PATH)
        _shi = _wbi.sheet_by_index(0)
        _hdr = [_shi.cell_value(0, _c) for _c in range(_shi.ncols)]
        _ix = _inv_pick(_hdr)
        for _ri in range(1, _shi.nrows):
            _inv_raw.append({k: _shi.cell_value(_ri, i) for k, i in _ix.items()})
        INV_NROWS = len(_inv_raw)
        INV_TRUNC = (INV_NROWS >= 65534)

inv_rows = []
for _rec in _inv_raw:
    mat = dnz(_rec['mat']).upper()
    if not mat:
        continue
    avail = fnum(_rec['qty']) - fnum(_rec['kept'])
    if avail <= 0:
        continue
    color = dnz(_rec['color'])
    if mat[:2] in ('39', '86') and color == '1':
        continue
    inv_rows.append({'mat': mat, 'color': color.upper(), 'w': fnum(_rec['w']),
                     'model': dnz(_rec['model']).upper(), 'unit': dnz(_rec['unit']),
                     'slot': dnz(_rec['slot']), 'in': _pdate(_rec['indate']),
                     'avail': avail})
print(f'庫存 {INV_NAME}：{INV_NROWS} 資料列（截斷疑慮={INV_TRUNC}）·可用池 {len(inv_rows)} 筆'
      + ('  ⛔ 4b 停判模式（庫存檔未提供·R-v545-1）' if INV_ABSENT else '  ✅ R-v545-2 表頭對應'))
inv_by_suffix = defaultdict(list)
for iv in inv_rows:
    inv_by_suffix[iv['mat'][2:] if len(iv['mat']) > 2 else iv['mat']].append(iv)

# ---------- 6b 重複開單群組 ----------
g6b = defaultdict(list)
for a in ANA:
    if a['is89']:
        r = a['row']
        k = (a['sc'] or a['code'], dnz(r[11]).upper(), dnz(r[12]).upper(), dnz(r[13]), dnz(r[14]).upper())
        g6b[k].append(a)
OBS_SET = {w['order'] for w in S6W}
RECHECK_ON = True          # R-0819-1（Amber 0819 裁-1 轉正·0826「A1-轉正」再確認·永久）：結案後仍在總表且未消耗之 89 一律回列 6b 復檢
S6B_RECHECK = []
n_6b_obs_pulled_back = 0
n_6b_obs_removed = 0
S6B, gid_n = [], 0
GID_ALL = {}
for k, items in sorted(g6b.items()):
    orders_all = {x['order'] for x in items}
    if len(items) < 2 or len(orders_all) < 2:
        continue
    survive = []
    for x in items:
        rec = ORDERS.get(x['order'])
        st = dnz(rec.get('status')) if rec else ''
        pc_closed = False
        raw6 = ''
        if rec:
            raw6 = dnz(rec.get('raw_reason'))
            hit = PC_MAP.get(_norm_raw(raw6))
            pc_closed = bool(hit and hit.get('status') == 'CLOSED')
        closed_ish = (st in ('CLOSED', 'PROCESSED') or pc_closed)
        unconsumed_x = (fnum(x['row'][21]) == 0 and fnum(x['row'][23]) == 0)
        if closed_ish and unconsumed_x and RECHECK_ON and x['order'] not in NO_RECHECK:   # R-0908-4
            # R-0819-1（Amber 林彥博 2026-08-19 裁-1「轉正·永久」·2026-08-26「A1-轉正」再確認）
            # amber_ruling：「之前審核案客戶預告數量增加備料並結案訂單，如果仍在系統上(進度總表)，
            #   請一律重新放回 6b.重複開單群組重新檢查以即時止損。」
            # 邊界：僅「仍 active 且未消耗(已交=0 且 保留=0)」者回列；已交/已保留者仍走 9.已結案移除。
            #   回列者同時豁免 R-v515-1（觀察中移除），否則止損目的落空。
            fam = '【預告增量結案】' if EXEMPT_RE.search(raw6) else ''
            x = dict(x, recheck='♻️結案後復檢(R-0819-1)' + fam,
                     recheck_src=(dnz(rec.get('disp_zh')) if rec else '') or st or 'CLOSED(語句)',
                     recheck_raw=raw6,
                     recheck_d=(dnz(rec.get('backfill_date')) if rec else ''),
                     recheck_fam=bool(fam))
            S6B_RECHECK.append(x)
            survive.append(x)
        elif closed_ish:
            S9.append((x, '6b', st or 'CLOSED(語句)', raw6,
                       dnz(rec.get('backfill_date')) if rec else ''))
        else:
            survive.append(x)
    _n0 = len(survive)
    survive2 = []
    for x in survive:
        if x['order'] in OBS_SET and not x.get('recheck'):
            continue
        if x['order'] in OBS_SET and x.get('recheck'):
            x['recheck'] = x['recheck'] + '·並自6觀察名單回列'
            n_6b_obs_pulled_back += 1
        survive2.append(x)
    survive = survive2
    n_6b_obs_removed += _n0 - len(survive)
    unconsumed = [x for x in survive if fnum(x['row'][21]) == 0 and fnum(x['row'][23]) == 0]
    if len({x['order'] for x in survive}) >= 2 and len({x['order'] for x in unconsumed}) >= 2:
        gid_n += 1
        GID_ALL[gid_n] = items      # R-0819-1 追加：保留該規格「全部 active 89」供 6c 垂直並列（含部分已交者）
        for x in survive:
            r2 = x['row']
            m2 = dnz(r2[11]).upper()
            c2 = dnz(r2[12]).upper()
            w2 = fnum(r2[13])
            md2 = dnz(r2[14]).upper()
            od2 = as_date(r2[4])
            mis = ''
            mis_iv = None
            for iv in inv_by_suffix.get(m2[2:] if len(m2) > 2 else m2, []):
                if not mat_compatible(m2, iv['mat']):
                    continue
                if abs(iv['w'] - w2) > 1e-9:
                    continue
                if md2 and iv['model'] and md2 != iv['model']:
                    continue
                if c2 not in ('', '1') and iv['color'] not in ('', '1') and c2 != iv['color']:
                    continue
                if od2 and iv['in'] and iv['in'] <= od2:
                    mis = '🟣有可用庫存仍開89 / Đã có tồn kho vẫn mở 89'
                    mis_iv = iv
                    break
            S6B.append((gid_n, len(survive), x, x in unconsumed, mis, mis_iv, x.get('recheck', '')))
print(f'6b={gid_n}群/{len(S6B)}列（R-v515-1 觀察中移除 {n_6b_obs_removed} 列）| 9.結案={len(S9)}')
# ---- R-0819-1 互斥鐵則：♻️復檢回列 6b 者不得同時列於 9.已結案移除 ----
# 由 dpr_regression_v0819_recheck A2 攔獲（0819 首跑）：Sheet6 候選迴圈亦會把 CLOSED 之未消耗 89
#   推入 S9，與 6b 復檢回列並存 → 同一單「既已結案移除又回列復檢」自相矛盾。
# 處置：凡實際落入 6b 群組且標♻️者，自 S9 剔除（未成群者不受影響·仍走 9 表，因單一規格無重複備料風險）。
_RCK_IN_6B = {t[2]['order'] for t in S6B if t[6]}
_n9_pull = sum(1 for x in S9 if x[0]['order'] in _RCK_IN_6B)
S9 = [x for x in S9 if x[0]['order'] not in _RCK_IN_6B]
print(f'R-0819-1 互斥：自 9.已結案移除 剔除 {_n9_pull} 列（已回列 6b 復檢）→ 9 表餘 {len(S9)} 列')

# ---- R-0819-1 附屬：重複備料曝險（6c）——垂直並列：該規格「全部未交完之 89」逐列展開 ----
# 可止損量口徑（不變）：僅以「未消耗(已交=0·保留=0)」之 89 計算 Σ未交 − 最大單未交；
#   已部分交貨/已保留者列為參考列（◽不計入可止損），但仍必須顯示，供人工檢查全部未交完之 89。
S6C = []
LOSS_BY_ORDER = {}
for gid in sorted(GID_ALL):
    items = GID_ALL[gid]
    open89 = [x for x in items if undel(x['row']) > 0]          # 未交完之 89（全部，不限未消耗）
    unc89 = [x for x in open89 if fnum(x['row'][21]) == 0 and fnum(x['row'][23]) == 0]
    if len(unc89) < 2:
        continue
    unds = [undel(x['row']) for x in unc89]
    tot = round(sum(unds), 1)
    mx = max(unds)
    loss = round(tot - mx, 1)
    if loss <= 0:
        continue
    keep = max(unc89, key=lambda x: undel(x['row']))
    rck_map = {t[2]['order']: t[6] for t in S6B if t[0] == gid}
    src_map = {t[2]['order']: t[2] for t in S6B if t[0] == gid}
    open89.sort(key=lambda x: (as_date(x['row'][4]) or datetime.date(1900, 1, 1)))
    x0 = open89[0]
    r0 = x0['row']
    dets = []
    for x in open89:
        rr = x['row']
        _od = as_date(rr[4])
        _unc = (fnum(rr[21]) == 0 and fnum(rr[23]) == 0)
        _st = ('未消耗(已交=0·保留=0) / Chưa tiêu thụ' if _unc
               else ('已保留 / Đã bảo lưu' if fnum(rr[23]) > 0 else '已部分交貨 / Đã giao một phần'))
        if not _unc:
            _vd = '◽已消耗·不計入可止損 / Đã tiêu thụ, không tính cắt lỗ'
        elif x is keep:
            _vd = '✅保留基準 / Giữ làm cơ sở'
        else:
            _vd = '⚠️建議止損 / Đề nghị cắt lỗ'
        _rck = rck_map.get(x['order'], '')
        _sx = src_map.get(x['order'])
        dets.append({'order': x['order'], 'stt': dnz(rr[3]), 'date': dstr(rr[4]),
                     'age': ((TODAY - _od).days if _od else ''), 'qty': fnum(rr[15]),
                     'done': fnum(rr[20]), 'giao': fnum(rr[21]), 'bl': fnum(rr[23]),
                     'und': undel(rr), 'state': _st, 'verdict': _vd, 'rck': _rck,
                     'rck_src': ((f"[{_sx.get('recheck_d','')}] {_sx.get('recheck_src','')}"
                                  f"｜原回填：{_sx.get('recheck_raw','')}") if (_sx and _rck) else ''),
                     'nv': x['nv'], 'tl': x['tl']})
    S6C.append({'gid': gid, 'code': x0['code'], 'sc': x0['sc'] or x0['code'],
                'mat': dnz(r0[11]), 'color': dnz(r0[12]), 'w': fnum(r0[13]), 'model': dnz(r0[14]),
                'n': len(unc89), 'n_open': len(open89), 'unit': dnz(r0[16]),
                'tot': tot, 'mx': mx, 'loss': loss, 'dets': dets,
                'nv': x0['nv'], 'tl': x0['tl'],
                'rck': sum(1 for d in dets if d['rck'])})
    for x in unc89:
        LOSS_BY_ORDER[x['order']] = loss
S6C.sort(key=lambda d: -d['loss'])
print(f'6c 重複備料曝險：{len(S6C)} 群 / {sum(d["n_open"] for d in S6C)} 列（未交完之89全列）'
      f'｜可止損合計 {round(sum(d["loss"] for d in S6C),1)}（原生單位混計·明細見分頁）')
print(f'R-0819-1 復檢回列：{len(S6B_RECHECK)} 列（其中【預告增量結案】家族 '
      f'{sum(1 for x in S6B_RECHECK if x.get("recheck_fam"))} 列；自6觀察名單回列 {n_6b_obs_pulled_back} 列）'
      f'｜實際落入 6b 群組 {sum(1 for t in S6B if t[6])} 列')

# ---------- 4b 主體 ----------
if 'sheet4_whitelist' in D:
    WL4 = D['sheet4_whitelist']
    assert len(WL4['entries']) >= int(WL4.get('ratchet_min', 0)), \
        f"R-v537-1 棘輪違例：白名單 {len(WL4['entries'])} < 下限 {WL4.get('ratchet_min')}"
    print(f"Sheet4 白名單：字典內建（R-v537-1·{len(WL4['entries'])} 筆·棘輪≥{WL4.get('ratchet_min')}）")
else:
    import glob as _g4
    _wl4c = sorted(_g4.glob('sheet4_whitelist_v*.json') + _g4.glob('/mnt/project/sheet4_whitelist_v*.json'))
    WL4 = _json.load(open(_wl4c[-1], encoding='utf-8'))
    print(f'Sheet4 白名單：{_wl4c[-1].split("/")[-1]}（standalone 後備）')
WL_89 = set()
WL_CM = set()
for e in WL4.get('entries', []):
    if dnz(e.get('order')):
        WL_89.add(dnz(e.get('order')))
    c = cust_code(e.get('cust'))
    m = dnz(e.get('MA')).upper()
    if c and m:
        WL_CM.add((c, m))
n4b_excl = {'closed': 0, 'proc': 0, 'window': 0, 'wl': 0}
S4B = []
for a in ANA:
    r = a['row']
    if a['is89'] or a['cat'] not in ('85', '86', '87', '88'):
        continue
    om = dnz(r[11]).upper()
    if 'DGT' in a['order']:
        continue
    if dnz(r[30]) not in ('', '0'):
        continue
    if fnum(r[23]) > 0:
        continue
    st4b, _ew4b = resolved_state(a['order'])
    if st4b == 'CLOSED':
        n4b_excl['closed'] += 1
        continue
    if st4b == 'PROCESSING':
        n4b_excl['proc'] += 1
        continue
    if st4b == 'WINDOW':
        n4b_excl['window'] += 1
        continue
    if (a['sc'], om) in WL_CM or (a['code'], om) in WL_CM:
        n4b_excl['wl'] += 1
        continue
    oc = dnz(r[12]).upper()
    ow = fnum(r[13])
    omod = dnz(r[14]).upper()
    od = as_date(r[4])
    hits = []
    for iv in inv_by_suffix.get(om[2:] if len(om) > 2 else om, []):
        if not mat_compatible(om, iv['mat']):
            continue
        if abs(iv['w'] - ow) > 1e-9:
            continue
        if omod and iv['model'] and omod != iv['model']:
            continue
        if oc not in ('', '1') and iv['color'] not in ('', '1') and oc != iv['color']:
            continue
        if od and iv['in'] and iv['in'] > od:
            continue
        hits.append(iv)
    hits.sort(key=lambda x: (x['in'] or datetime.date(1900, 1, 1)))
    for iv in hits[:3]:
        unit_ok = '一致' if dnz(r[16]) == iv['unit'] else '⚠️單位不一致·需人工判定 / Đơn vị khác, cần XN'
        S4B.append((a, iv, unit_ok, len(hits)))
print(f'4b前置排除={n4b_excl}')
print(f'4b={len(S4B)}列（{len({(x[0]["order"], dnz(x[0]["row"][3])) for x in S4B})}單線）')

# ---------- Sheet4 現檔判定（R-v528-3） ----------
by_key_89 = defaultdict(list)
for a in ANA:
    if a['is89']:
        r = a['row']
        k4 = (a['sc'] or a['code'], dnz(r[11]).upper(), dnz(r[12]).upper(), fnum(r[13]), dnz(r[14]).upper())
        d4 = as_date(r[4])
        if d4:
            by_key_89[k4].append((d4, a))
S4 = []
n4_excl = {'sameday': 0, 'dc': 0, 'bl': 0, 'wl': 0, 'dgt': 0, '已結案': 0, '處理中': 0, '窗內': 0, '89已結/處理': 0,
           '未交<200不可取用': 0}
n4_verdict = Counter()


def undel_verdict(rf, r89):
    """R-v561-2＋R-0918-8：以 89 之未交數量（換算至正式單單位）對照正式訂單數量三分流。"""
    q = fnum(rf[15])
    u = undel(r89)
    uf, u89 = dnz(rf[16]), dnz(r89[16])
    spec = (dnz(r89[11]).upper(), fnum(r89[13]), dnz(r89[14]).upper())
    uc, how = conv_qty(u, u89, uf, spec)
    if uc is None:
        return 'unit_na', u, q, ('⚠️單位不一致(%s vs %s)·%s·不排除·待裁決(R-0918-8) / '
                                 'ĐV khác loại, chưa quy đổi được, không loại trừ'
                                 % (uf or '(空)', u89 or '(空)', how))
    note = ('｜' + how) if how else ''
    if uc >= q:
        return 'full', u, q, note
    if u < UNDEL_MIN:
        return 'tiny', u, q, note
    return 'partial', u, q, note


for a in ANA:
    if a['is89'] or a['cat'] not in ('85', '86', '87', '88'):
        continue
    r = a['row']
    k4 = (a['sc'] or a['code'], dnz(r[11]).upper(), dnz(r[12]).upper(), fnum(r[13]), dnz(r[14]).upper())
    cands4 = by_key_89.get(k4)
    if not cands4:
        continue
    fd4 = as_date(r[4])
    if not fd4:
        continue
    earlier4 = [(d, x) for d, x in cands4 if d < fd4]
    if not earlier4:
        if any(d == fd4 for d, _x in cands4):
            n4_excl['sameday'] += 1
        continue
    if 'DGT' in a['order']:
        n4_excl['dgt'] += 1
        continue
    if dnz(r[30]) not in ('', '0'):
        n4_excl['dc'] += 1
        continue
    if fnum(r[23]) > 0:
        n4_excl['bl'] += 1
        continue
    d89_4, x89_4 = max(earlier4, key=lambda t: t[0])
    if (x89_4['order'] in WL_89 or (a['sc'], k4[1]) in WL_CM or (a['code'], k4[1]) in WL_CM):
        n4_excl['wl'] += 1
        continue
    _vd, _un4, _qf4, _note4 = undel_verdict(r, x89_4['row'])
    if _vd == 'tiny':
        n4_excl['未交<200不可取用'] += 1
        continue
    n4_verdict[_vd] += 1
    st_f, ew_f = resolved_state(a['order'])
    if st_f == 'CLOSED':
        n4_excl['已結案'] += 1
        continue
    if st_f == 'PROCESSING':
        n4_excl['處理中'] += 1
        continue
    if st_f == 'WINDOW':
        n4_excl['窗內'] += 1
        continue
    st_9, _ = resolved_state(x89_4['order'])
    if st_9 in ('CLOSED', 'PROCESSING'):
        n4_excl['89已結/處理'] += 1
        continue
    S4.append((a, x89_4, fd4, d89_4, {'v': _vd, 'und': _un4, 'qf': _qf4, 'note': _note4}))
print(f'Sheet4(R-v528-3 現檔判定)={len(S4)}群/{len(S4)*2}列｜豁免={n4_excl}'
      f'｜R-v561-2 分流={dict(n4_verdict)}')

# ---------- 7w / Sheet8 ----------
S7W_ALL = sorted({(a['code'], a['sc']) for a in ANA if not a['bc']})
# R-0916-4：白名單內者不進 7w 計數，但於分頁末段具名列示（抑制≠隱藏）
S7W = [x for x in S7W_ALL if x[0] not in SUPPRESS_7W]
S7W_SUP = [x for x in S7W_ALL if x[0] in SUPPRESS_7W]
mats_seen = {}
for a in ANA:
    m = dnz(a['row'][11]).upper()
    if m and m not in NTNS and m not in mats_seen and not EXC_RE.match(m):
        mats_seen[m] = (dnz(a['row'][12]), a['code'], a['sc'], a['nv'])   # R-0819-7：99Z 家族不得入表
S8 = sorted(mats_seen.items())
print(f'7w={len(S7W)}（白名單抑制 {len(S7W_SUP)}·R-0916-4） Sheet8={len(S8)}（v{NTNS_VER} 採認態）')

# ---------- stage dumps ----------
with open('_stage.pkl', 'wb') as f:
    pickle.dump({'NTNS': NTNS, 'active': [a['row'] for a in ANA]}, f)
import pandas as pd
pd.DataFrame({
    'k': range(len(ANA)),
    '訂單號碼\nMã đơn': [a['order'] for a in ANA],
    '_yarn': [a['yarn'] for a in ANA],
    '_no_update': [(a['no_update'] and not a['is89']) for a in ANA],
    '_prog_same': [(a['prog_same'] and not a['is89']) for a in ANA],
    '_risk_level': [a['risk'] for a in ANA],
    '_f_major': [a['major'] for a in ANA],
}).to_pickle('active_0622.pkl')
print('PART2 OK')

# ==================== PART 3 輸出簿 ====================
import openpyxl
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.utils import get_column_letter

THIN = Side(style='thin', color='FF000000')
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
F_HDR = PatternFill('solid', fgColor='FFD9D9D9')
F_YEL = PatternFill('solid', fgColor='FFFFFF00')
F_BLU = PatternFill('solid', fgColor='FFDDEBF7')
F_GRY = PatternFill('solid', fgColor='FFF2F2F2')
F_PUR = PatternFill('solid', fgColor='FFE4D7F5')
F_UNC = PatternFill('solid', fgColor='FFFCE4D6')
F_WAVE = PatternFill('solid', fgColor='FFFFE699')
F_STAT_HL = PatternFill('solid', fgColor='FFF4CCCC')   # R-0904-2：製程站別高風險列
RISK_FILL = {HIGH: PatternFill('solid', fgColor='FFFFC7CE'), MEDH: PatternFill('solid', fgColor='FFFFCC99'),
             MED: PatternFill('solid', fgColor='FFFFEB9C'), LOW: PatternFill('solid', fgColor='FFF2F2F2')}
BOLD = Font(bold=True)

wb = openpyxl.Workbook()
wb.remove(wb.active)
TAB_COUNTS = {}


# ══ R-0908-1（Amber 林彥博 2026-09-08）百分比欄位一律顯示為 _% ══
# amber_ruling：「2.統計 Thống kê 和 2b.產品別準交率 OTD theo SP 只要是百分比的欄位都一律顯示為_%」
# 落地方式：**純呈現層**——儲存格值仍為數值（如 60.6），只加 number_format 讓 Excel 顯示 60.6%。
#   ⒜ 不改成字串 '60.6%'：否則排序/篩選/後續讀取全部失效（回歸棒亦讀不到數值）。
#   ⒝ 不用內建 '0.0%' 格式：內建 % 會把值再乘 100（60.6 → 6060.0%），故用引號字面量 '0.0"%"'。
#   ⒞ '—'（None 之佔位字串）為文字，套用格式無副作用。
PCT_FMT = '0.0"%"'


def put(ws, r, c, v, fill=None, bold=False, wrap=False, txt=False, pct=False):
    if isinstance(v, str):
        v = ILLEGAL.sub('', v)
    cell = ws.cell(r, c, v)
    cell.border = BORDER
    if fill:
        cell.fill = fill
    if bold:
        cell.font = BOLD
    if wrap:
        cell.alignment = Alignment(wrap_text=True, vertical='top')
    if txt:
        cell.number_format = '@'
    if pct and isinstance(v, (int, float)) and not isinstance(v, bool):
        cell.number_format = PCT_FMT      # R-0908-1
    return cell


def zhh(h):
    return dnz(h).split(' / ')[0].split('\n')[0].strip()


def write_table(ws, hdr, rows, start=1, hdr_fill=F_HDR):
    zh_list = [zhh(h) for h in hdr]
    code_j = zh_list.index('客戶代碼') + 1 if '客戶代碼' in zh_list else 0
    for j, h in enumerate(hdr, 1):
        put(ws, start, j, h, fill=hdr_fill, bold=True)
    for i, row in enumerate(rows, start + 1):
        for j, v in enumerate(row, 1):
            put(ws, i, j, v, txt=(j == code_j))
    ws.auto_filter.ref = f'A{start}:{get_column_letter(len(hdr))}{start+len(rows)}'


def autowidth(ws, cap=60):
    w = {}
    for row in ws.iter_rows():
        for c in row:
            if c.value is None:
                continue
            s = str(c.value)
            if c.number_format == PCT_FMT:
                s += '%'                     # R-0908-1：顯示寬度含 %
            ln = sum(2 if ord(ch) > 255 else 1 for ch in s[:80])
            w[c.column] = min(max(w.get(c.column, 8), ln + 2), cap)
    for col, width in w.items():
        ws.column_dimensions[get_column_letter(col)].width = width


BF_HDRS = ['異常原因檢查 / Báo cáo kiểm tra', '處理方式和結果 / Cách xử lý & kết quả',
           '憑證單號(選填) / Mã chứng từ (tùy chọn)',
           '處理進度 / Tiến độ xử lý', '舊回填紀錄(歷史) / Hồ sơ báo cáo cũ']


def bf_cells(ws, r, base_c, prog, old, old_d):
    put(ws, r, base_c, '', fill=F_YEL)
    put(ws, r, base_c + 1, '', fill=F_YEL)
    put(ws, r, base_c + 2, '', fill=F_YEL)
    put(ws, r, base_c + 3, prog, fill=F_BLU, wrap=True)
    put(ws, r, base_c + 4, (f'[{old_d}] {old}' if old else ''), fill=F_GRY, wrap=True)


# ---------- 0.說明 ----------
ws0 = wb.create_sheet('0.說明')
NOTES = [
    (f'{GROUP} 每日訂單進度追蹤 — {TODAY.strftime("%Y/%m/%d")} 分析（SKILL v3.5 · 權威快照 v{PRE["snapshot_version"]} · 字典 v{DICT_VER} · NT/NS v{NTNS_VER} · 庫存 {INV_NAME}）', True),
    ('母體：原始 %d → (訂單號,#2,料號,色號,類別)去重 %d → active(未完成) %d，其中 89 預告 %d（R-v522-2 不列進度異常）' % (n_raw, n_dedup, len(ANA), n89), False),
    ('門檻：樣品 DELAY≥14/警告≥10；量產 DELAY≥30/警告≥21；過1.9(Mail二次判定)/過客戶交期/測試F=DELAY；寬限：下單≤2天且1.9空=OK', False),
    ('風險：🔴DELAY+(過客戶交期/缺紗/測試F)｜🟠DELAY或WARNING+缺紗｜🟡WARNING｜⚪POTENTIAL；⭐KN/LL/XLBT 與 🆘缺紗+停滯 強制🔴且覆蓋寬限', False),
    ('', False),
    (f'★ ⏰ {WAVE_MMDD} 到期潮（明日·R-v515-1 回歸路徑）：6觀察名單監控到期 ≤{WAVE_DATE} 者本輪 {n_wave} 單已加⏰前綴並置頂。', True),
    ('  → 到期日起無後單/無消耗證據者整批自動回歸 6/6b 回填表（⏰標記）。請助理今日預先處置：有單（掛用/消耗證據）→結案；無單→移轉/報廢二選一（cap🛑三選一另計）。', False),
    ('  → Chuẩn bị trước: đơn theo dõi hết hạn sẽ tự động quay lại báo cáo (R-v515-1). Có đơn → kết án; chưa có đơn → chuyển tổ hoặc hủy bỏ. Hạn chót chỉ là đề xuất.', False),
    ('★ R-v525-2（Amber 0714）：「KHÔNG CÓ ĐƠN DÙNG/SD」（現無單使用·≠KHÔNG CÒN 死預告）依帳齡 90 天分流：≤90 天→OPEN 觀察；>90 天→直接 FORCE 三選一·不入觀察。', True),
    ('★ R-v522-1/2（Amber 0714）：全表表頭中越並列；業務姓名中越並列（R-v528-1 已正名）；89 預告一律不列進度異常、不帶⭐/🆘，統計已排除。', False),
    ('', False),
    ((f'★ R-v528-3（Amber 0715 二次指示）：Sheet4 現檔判定——以當日檔內「正式單×同規格 active 89」直接配對'
      f'（配對鍵＝客戶+料號+色號+寬度+型號·取最近且嚴格早於正單之 89）；異常＝正單嚴格晚於89 且 DC完全未掛 且 保留=0。'
      f'本輪實判 {len(S4)}群/{len(S4)*2}列；同日SOP {n4_excl["sameday"]}／已掛DC {n4_excl["dc"]}／保留>0 {n4_excl["bl"]}／白名單 {n4_excl["wl"]}／DGT {n4_excl["dgt"]} 豁免。'), True),
    ((f'★ R-v527-1（Amber 0715·僅轄 4s）：覆蓋率基準——89DB 累積起始 {COV["start"]}，本輪覆蓋 {COV["covered"]}/{COV["total"]}'
      f'（或 12 支歷史檔齊備·現 {PRE["interval_89_files"]}/12），達標即解除 4s 佔位。'), True),
    ('  → 4s.共用89餘量不足 本輪佔位：系統資料待補·非異常 / Dữ liệu hệ thống chờ bổ sung, không tính lỗi trợ lý。', False),
    ('★ R-v529-1（Amber 0715）：觀察一期 15 天——monitor_until＝回填/裁決日＋15；期內不重複詢問，到期才回歸複查。', False),
    (('★ R-v561-1（Amber 林彥博 2026-08-03）：所有列訂單之分頁新增「未交數量」欄＝訂單數量 − 已交（原生單位）。'
      '⛔ 禁用「未交折合碼」對照。 / Tất cả các bảng có đơn đều thêm cột「SL chưa giao」= SL đơn − đã giao (đơn vị gốc).'), True),
    ((f'★ R-v561-2（Amber 林彥博 2026-08-03）：Sheet4 以 89 之未交數量對照正式訂單數量三分流——'
      f'ⓐ未交≥正式單＝可整單取用→異常；ⓑ未交<200<正式單＝不可取用·非異常（排除·本輪 {n4_excl["未交<200不可取用"]} 群）；'
      f'ⓒ200≤未交<正式單＝無法整單取用但剩餘過多→列異常並由人工判定。本輪分流={dict(n4_verdict)}'), True),
    ((f'★ R-v532-1（Amber 0716）：已回填不重複詢問——Sheet4/4b/6/6b 統一豁免。'
      f'本輪 Sheet4 豁免 已結{n4_excl["已結案"]}／處理中{n4_excl["處理中"]}／窗內{n4_excl["窗內"]}／89已結或處理{n4_excl["89已結/處理"]}；'
      f'4b 豁免 結案{n4b_excl["closed"]}／處理中{n4b_excl["proc"]}／窗內{n4b_excl["window"]}。'), True),
    (('★★ R-0819-1（Amber 林彥博 2026-08-19 裁-1·2026-08-26「A1-轉正」再確認·**轉正·永久**）結案後復檢：'
      '「之前審核案客戶預告數量增加備料並結案訂單，如果仍在系統上(進度總表)，請一律重新放回 6b.重複開單群組重新檢查以即時止損。」'
      f'落地＝凡已結案(CLOSED/PROCESSED/語句結案)但仍 active 且未消耗(已交=0·保留=0)之 89，一律回列 6b 並標♻️，'
      f'同時豁免 R-v515-1 觀察中移除。本輪回列 {len(S6B_RECHECK)} 列（其中【預告增量結案】家族 '
      f'{sum(1 for x in S6B_RECHECK if x.get("recheck_fam"))} 列、自 6觀察回列 {n_6b_obs_pulled_back} 列）。'
      '已交/已保留者仍走 9.已結案移除，不回列。新增分頁 6c.重複備料曝險 量化可止損量。 / '
      'R-0819-1: đơn DB 89 đã đóng nhưng vẫn trên bảng tiến độ & chưa tiêu thụ phải quay lại bảng 6b để rà soát, '
      'nhằm cắt lỗ chuẩn bị NVL trùng.'), True),
    (('★★ R-0820-1（Amber 林彥博 2026-08-20「落回」·2026-08-26「A2-轉正」·**轉正·永久**）觀察到期自動落回：'
      '「裁-B, 落回」——6觀察名單中 monitor_until 已過期且非 cap🛑 者，本輪起**自觀察名單移出、'
      f'直接落回 6.預告未保留使用 回填表**（生命週期＝⏰到期回歸），並改列派工「強制」。'
      f'本輪落回 {n_fallback} 單。舊行為（僅加 ⏰ 前綴、留在觀察名單、派工「預警」）自本輪起廢止——'
      '0819→0820 實測到期分佈完全相同、一日之內零處置，證明留在觀察名單不會被處理。'
      'cap🛑 不受影響（本即走 R-v492-1 強制三選一）。 / '
      'R-0820-1: đơn theo dõi quá hạn sẽ tự động quay lại bảng 6 và chuyển sang phân công BẮT BUỘC.'), True),
    (('★ R-0820-2（Amber 林彥博 2026-08-20）ERP 匯出空列：「空白是倒出資料異常，請忽略」——'
      '進度表中訂單號空白之列屬匯出端異常，已於 R-v552-1 去重階段剔除，不列異常、不追問、不計入任何統計。 / '
      'Dòng trống trong file xuất ERP là lỗi xuất dữ liệu, đã loại bỏ, không tính bất thường.'), True),
    ('★ R-v529-2（Amber 0715）：主管提問原文保留為📌待辦，恆顯示於 Sheet6「📌主管提問」＋6b 原列；系統不改寫、不自動結案、不入觀察。', False),
    ('★ NT/NS：v%d 採認態（R-v496-1 精確全碼·嚴禁前綴推導）。68QE523VA=NT/68QE756VA=NT/81TB527VM=NS 入保護欄；留白待判：%s（勿臆測）。' % (NTNS_VER, '／'.join(sorted(PENDING_BLANK))), True),
    ('  → 8.NTNS未分類 %d 料號待人工判定後回傳、本輪不派工 / chờ phân loại thủ công, không phân công。' % len(S8), False),
    (('★ R-0819-7（Amber 林彥博 2026-08-19·轉正·永久）：99Z 家族（99Z01/02/03/19）＝特殊品名／加工單號，'
      '無單一 NT/NS 屬性 → **不得入 8.NTNS未分類**、亦不寫入字典 keys；1.主分析 NT/NS 欄標示排除依據。'
      '與 R-v496-1 嚴禁前綴推導不衝突（本規則不賦值·僅宣告不進分類流程）。留白待判僅餘 81H55002V。 / '
      'Nhóm 99Z là tên SP đặc biệt hoặc mã gia công, không có thuộc tính NT/NS → không đưa vào bảng 8.'), True),
    ('', False),
    (('★★ R-0908-4（Amber 林彥博 2026-09-08·具名裁決）結案後復檢·個案豁免：'
      '「合理回報，請結案不要再複查」——Amber 於 0908 回傳檔 6b 逐列具名審閱後認定回填合理，'
      '該批 89 ⒜結案 ⒝不再依 R-0819-1 回列 6b 復檢，改列 9.已結案移除。'
      '⚠️ 範圍僅限字典 no_recheck_orders 逐一具名之單號（R-0819-2 不泛化）；'
      'R-0819-1 規則本身仍為轉正·永久，未具名之結案未消耗 89 續一律回列復檢。'
      '⚠️ 本項為帳面結案，不等於實體止損——該批 89 於進度總表之未交量仍在，'
      '下批備料表之「89未交量」仍須人工確認是否計入。 / '
      'R-0908-4: các đơn DB 89 được Amber duyệt là hợp lý sẽ đóng và KHÔNG rà soát lại ở bảng 6b, '
      'chuyển sang bảng 9. Chỉ áp dụng cho các mã đơn được nêu đích danh.'), True),
    ('', False),
    (('★★ R-0908-1（Amber 林彥博 2026-09-08·轉正·永久）百分比欄位顯示：'
      '「2.統計 Thống kê 和 2b.產品別準交率 OTD theo SP 只要是百分比的欄位都一律顯示為 _%」——'
      '2.統計 之 DC比例／保留比例／準交率／有DC準交率／無DC準交率／有保留準交率／無保留準交率／DELAY率，'
      '及 2b 之 準交率／有DC比例／保留比例（含品名Top30）全部套用 0.0"%" 顯示格式。'
      '**儲存格值不變（仍為數值·可排序可篩選），只是顯示帶 %**；未算出者顯示「—」。'
      '異常判定與 OTD 計算一行未動。 / '
      'R-0908-1: các cột tỷ lệ % ở sheet 2 và 2b đều hiển thị kèm dấu %; giá trị ô không đổi.'), True),
    ('', False),
    (('★★ R-0904-2（Amber 林彥博 2026-09-04·轉正·永久）製程站別對照表補冊：'
      '「92-=卷紗／94-=染色／96-=打束頭／98-=特殊加工(具體加工類型看子代碼)」——'
      '連同既有 93-織造／95-胚帶後製程／97-品檢包裝，七碼全數入冊，「待確認·不臆測」自本輪起歸零。'
      '1.主分析 新增「今日站別」欄（98 附掛子代碼原文·不往上歸併）；2.統計 新增「製程站別 × 異常等級」區塊。 / '
      'R-0904-2: bổ sung bảng đối chiếu công đoạn — 92 đánh suốt / 93 dệt / 94 nhuộm / 95 hoàn thiện / '
      '96 bấm đầu dây / 97 KCS & đóng gói / 98 gia công đặc biệt (loại cụ thể xem mã con).'), True),
    ('  → 進度欄格式：[製程碼]-[狀態後綴] [日期 時間]；後綴 -0＝完工 Hoàn thành／-1＝生產中 Đang SX。', False),
    (('★★ R-0904-3（Amber 林彥博 2026-09-04·轉正·永久）分頁順序——「所有須人工回填的 Sheets 一律放在最前面，'
      '不須回填的向後放」。判定為機械式：表頭含回填欄（異常原因檢查／處理方式和結果／憑證單號／處理進度）'
      '或人工填欄者即入回填區。'
      '順序＝⬛0.說明（封面）→ 🟥回填區 7 頁（4／4b／6／6b／6c／7w／8）→ 🟧派工清單（指派入口）'
      '→ 🟦唯讀分析 9 頁（1.主分析／2／2b／3／4w／4s／6觀察／9／分類彙總）。'
      '頁籤配色同組：紅＝待回填、橘＝指派、藍＝唯讀、灰＝封面。 / '
      'R-0904-3: các sheet cần điền tay xếp trước (nền đỏ), sheet chỉ đọc xếp sau (nền xanh).'), True),
    ('  → ⚠️ 1.主分析 自本輪起位於🟦唯讀區（第 10 頁），非第 2 頁；請以頁籤顏色定位。 / '
     'Bảng 1.Phân tích chính nay nằm ở khu chỉ đọc (nền xanh), không còn ở vị trí thứ 2.', False),
    ('', False),
    ('回填版面 v514（兩欄·皆反黃待填）：①異常原因檢查/Báo cáo kiểm tra；②處理方式和結果/Cách xử lý & kết quả；③憑證單號(選填·R-v567-17)；後接 處理進度(系統判定)、舊回填紀錄(歷史)。', False),
    ('★ R-v515-1：已入 6觀察名單之單不留回填表（6/6b）；6b 觀察中成員移除、群組剩<2單整組退出；到期未結自動回歸回填表（⏰標記）。', False),
    ('4b 前置排除：結案/已處理 %d 筆、白名單雙鍵 %d 筆；「已掛89=非異常」「保留量>0=非異常(R-v487-1)」鐵則續用。' % (n4b_excl['closed'], n4b_excl['wl']), False),
    ('越南職場原則：異常一律框定為流程/系統缺口，不指向個人；回饋經 Amber/正式管道；VP 報告僅用客戶簡稱；限期均為建議值非承諾。', False),
    ('Nguyên tắc: mọi bất thường là lỗ hổng quy trình/hệ thống, không quy trách nhiệm cá nhân; phản hồi qua kênh chính thức; hạn chót chỉ là đề xuất.', False),
]
for i, (t, b) in enumerate(NOTES, 1):
    put(ws0, i, 1, t, bold=b, wrap=True)
ws0.column_dimensions['A'].width = 120
TAB_COUNTS['0.說明'] = len(NOTES)

# ---------- 1.主分析 ----------
ws1 = wb.create_sheet('1.主分析')
ws1.sheet_properties.tabColor = 'FF4472C4'
DERIVED = ['NT/NS', '風險等級 / Mức rủi ro', '異常等級 / Cấp bất thường', '異常原因 / Nguyên nhân bất thường',
           '建議處置 / Đề xuất xử lý', '客戶簡稱 / Tên tắt KH', '品牌代碼 / Mã nhãn',
           '品牌名稱 / Tên nhãn', '品牌PM / PM nhãn',
           # R-0904-2（Amber 0904）：製程站別對照表補冊 → 今日進度碼可解為站別（append·不動既有欄序）
           '今日站別 / Công đoạn hôm nay']
_H0 = [h.replace('\n', ' ') for h in HDR]
H_MAIN = _H0[:23] + [UNDEL_HDR] + _H0[23:] + DERIVED
for j, h in enumerate(H_MAIN, 1):
    put(ws1, 1, j, h, fill=F_HDR, bold=True)
DATE_COLS = {4, 5, 6, 7, 29}
r_i = 2
for a in ANA:
    r = a['row']
    for j in range(NCOLS):
        v = r[j]
        if j in DATE_COLS:
            v = dstr(v)
        elif isinstance(v, str):
            v = dnz(v)
        if j == 43:
            v = a['tl']
        elif j == 44:
            v = a['nv']
        put(ws1, r_i, j + 1 if j <= 22 else j + 2, v)
    put(ws1, r_i, 24, undel(r))
    base = NCOLS + 1
    nt = a['ntns']
    mat = dnz(r[11]).upper()
    if not nt and mat:
        if EXC_RE.match(mat):
            nt = EXC_TXT                                   # R-0819-7 排除類
        elif mat in PENDING_MATS:
            nt = '留白待Amber裁決 / Chờ Amber phán quyết'
        else:
            nt = '待人工判定 / Chờ XN'
    put(ws1, r_i, base + 1, nt)
    put(ws1, r_i, base + 2, a['risk'], fill=RISK_FILL.get(a['risk']))
    put(ws1, r_i, base + 3, a['level'])
    put(ws1, r_i, base + 4, a['reasons'], wrap=True)
    put(ws1, r_i, base + 5, a['disp'], wrap=True)
    put(ws1, r_i, base + 6, a['sc'])
    put(ws1, r_i, base + 7, a['bc'])
    put(ws1, r_i, base + 8, a['bn'])
    put(ws1, r_i, base + 9, a['pm'])
    put(ws1, r_i, base + 10, station_of(r[18]))   # R-0904-2：18=今日進度
    if a['is89'] or a['risk'] == OKR:
        ws1.row_dimensions[r_i].hidden = True
    r_i += 1
ws1.freeze_panes = 'D2'
ws1.auto_filter.ref = f'A1:{get_column_letter(NCOLS+11)}{r_i-1}'
TAB_COUNTS['1.主分析'] = r_i - 2

from collections import defaultdict as _dd_stat
defaultdict = _dd_stat
# ---------- 2.統計 ----------
ws2 = wb.create_sheet('2.統計')
row = 1
n_non89 = len(ANA) - n89
put(ws2, row, 1, '整體異常等級（active %d·排除89預告 %d 筆·R-v522-2）/ Cấp bất thường (loại trừ DB 89)' % (n_non89, n89), bold=True)
row += 1
for lv in ('DELAY', 'WARNING', 'POTENTIAL', 'OK'):
    put(ws2, row, 1, lv)
    put(ws2, row, 2, C.get(lv, 0))
    row += 1
put(ws2, row, 1, '⭐最優先(KN/LL/XLBT)')
put(ws2, row, 2, sum(a['prio'] for a in ANA))
row += 1
put(ws2, row, 1, '🆘重大異常(缺紗+停滯)')
put(ws2, row, 2, sum(a['major'] for a in ANA))
row += 2
put(ws2, row, 1, 'DELAY 依類別 / DELAY theo loại', bold=True)
row += 1
dc = Counter(('量產' if a['cat'] == '88' else '樣品') for a in ANA if a['level'] == 'DELAY' and not a['is89'])
for k in ('量產', '樣品'):
    put(ws2, row, 1, k)
    put(ws2, row, 2, dc.get(k, 0))
    row += 1
put(ws2, row, 1, '預告89')
put(ws2, row, 2, '—(R-v522-2 不列異常 / không tính bất thường)')
row += 2
put(ws2, row, 1, '各客戶 DELAY Top15（排除89預告）/ Top15 KH theo DELAY', bold=True)
row += 1
cc = Counter((a['sc'] or a['code']) for a in ANA if a['level'] == 'DELAY' and not a['is89'])
put(ws2, row, 1, '客戶簡稱 / Tên tắt KH', fill=F_HDR, bold=True)
put(ws2, row, 2, 'DELAY數 / Số DELAY', fill=F_HDR, bold=True)
row += 1
for k, v in cc.most_common(15):
    put(ws2, row, 1, k)
    put(ws2, row, 2, v)
    row += 1
row += 1
put(ws2, row, 1, '品牌 PM 集中度（DELAY·排除89預告）/ Tập trung theo PM nhãn', bold=True)
row += 1
pmc = Counter((a['pm'] or '(無PM)') for a in ANA if a['level'] == 'DELAY' and not a['is89'])
for k, v in pmc.most_common(10):
    put(ws2, row, 1, k)
    put(ws2, row, 2, v)
    row += 1

row += 1
put(ws2, row, 1, '★ 保留預告(已掛89/DC)·保留成品(保留量>0) 比例與準交率 ｜ 口徑＝內部從嚴 L2'
                 '（1.9優先·未設用標準期·Mail不救·無基準排除·89不進分母·寬限窗排除）'
                 ' / Tỷ lệ có DC & có bảo lưu và tỷ lệ giao đúng hạn (OTD)', bold=True, wrap=True)
row += 1
put(ws2, row, 1, '⚠️ 單檔快照＝時點代理指標，非跨期真實 OTD；跨期比較請走 KPI 深度分析'
                 ' / Chỉ số tại một thời điểm, không phải OTD thực theo kỳ', wrap=True)
row += 1
_OH = ['類別# / Loại#', '筆數 / Số nét', '有預告DC / Có DC', 'DC比例 / Tỷ lệ DC',
       '保留成品 / Có bảo lưu', '保留比例 / Tỷ lệ BL', 'OTD分母 / Mẫu số',
       'OTD準時 / Đúng hạn', '準交率 / OTD', '有DC準交率 / OTD có DC',
       '無DC準交率 / OTD không DC', '有保留準交率 / OTD có BL', '無保留準交率 / OTD không BL']
for _i, _h in enumerate(_OH, 1):
    put(ws2, row, _i, _h, fill=F_HDR, bold=True, wrap=True)
row += 1
_ALL = [a for a in ANA if not a['is89']]
CAT_OTD = {}
for _c in ('85', '86', '87', '88', '全體'):
    _g = _ALL if _c == '全體' else [a for a in _ALL if a['cat'] == _c]
    if not _g:
        continue
    _n = len(_g)
    _dc = sum(1 for a in _g if a['has_dc'])
    _kp = sum(1 for a in _g if a['kept'])
    _d, _num, _rt = otd_rate([(a['otd'][0], a['otd'][1]) for a in _g])
    _r_dc = otd_rate([(a['otd'][0], a['otd'][1]) for a in _g if a['has_dc']])[2]
    _r_nd = otd_rate([(a['otd'][0], a['otd'][1]) for a in _g if not a['has_dc']])[2]
    _r_kp = otd_rate([(a['otd'][0], a['otd'][1]) for a in _g if a['kept']])[2]
    _r_nk = otd_rate([(a['otd'][0], a['otd'][1]) for a in _g if not a['kept']])[2]
    CAT_OTD[_c] = {'n': _n, 'dc': _dc, 'kept': _kp, 'den': _d, 'num': _num, 'otd': _rt,
                   'otd_dc': _r_dc, 'otd_ndc': _r_nd, 'otd_kp': _r_kp, 'otd_nkp': _r_nk}
    _pc = lambda v: ('—' if v is None else round(v * 100, 1))
    for _i, _v in enumerate([_c, _n, _dc, _pc(_dc / _n), _kp, _pc(_kp / _n), _d, _num,
                             _pc(_rt), _pc(_r_dc), _pc(_r_nd), _pc(_r_kp), _pc(_r_nk)], 1):
        put(ws2, row, _i, _v, bold=(_c == '全體'), fill=(F_BLU if _c == '全體' else None),
            pct=(_i in (4, 6, 9, 10, 11, 12, 13)))   # R-0908-1
    row += 1
_g88, _g85 = CAT_OTD.get('88'), CAT_OTD.get('85')
if _g88 and _g88['otd'] is not None and _g88['otd_dc'] is not None and _g88['otd_ndc'] is not None:
    _delta = round((_g88['otd_dc'] - _g88['otd_ndc']) * 100, 1)
    put(ws2, row, 1, '判讀：88量產「有DC」vs「無DC」準交率差 %+.1f 個百分點 —— %s'
                     ' / Chênh lệch OTD giữa có DC và không DC'
        % (_delta, '掛預告確實拉高準交率，備料機制有效'
           if _delta > 0 else '掛預告未帶來準交率優勢，須查預告品質而非數量'), wrap=True)
    row += 1
row += 1
# ══ R-0904-2（Amber 0904）製程站別 × 異常等級（排除 89 預告）══
put(ws2, row, 1, '製程站別 × 異常等級（active 非89·依今日進度碼 R-0904-2 對照表）'
                 ' / Công đoạn × cấp bất thường', bold=True, wrap=True)
row += 1
for _i, _v in enumerate(['製程站別 / Công đoạn', '筆數 / Số nét', 'DELAY', 'WARNING',
                         'POTENTIAL', 'OK', 'DELAY率 / Tỷ lệ DELAY(%)'], 1):
    put(ws2, row, _i, _v, fill=F_HDR, bold=True)
row += 1
_ST = defaultdict(lambda: {'n': 0, 'DELAY': 0, 'WARNING': 0, 'POTENTIAL': 0, 'OK': 0})
for _a in ANA:
    if _a['is89']:
        continue
    _st = station_of(_a['row'][18])
    _st = _st.split('·子代碼')[0]          # 98 於本表歸併顯示；子代碼明細見 1.主分析
    _lv = dnz(_a['level']).split(' /')[0].split(' ')[0]
    _ST[_st]['n'] += 1
    if _lv in _ST[_st]:
        _ST[_st][_lv] += 1
for _st, _d in sorted(_ST.items(), key=lambda x: -x[1]['n']):
    _rate = round(_d['DELAY'] / _d['n'] * 100, 1) if _d['n'] else '—'
    _hl = F_STAT_HL if (_d['n'] >= 30 and _d['DELAY'] / _d['n'] >= 0.30) else None
    for _i, _v in enumerate([_st, _d['n'], _d['DELAY'], _d['WARNING'],
                             _d['POTENTIAL'], _d['OK'], _rate], 1):
        put(ws2, row, _i, _v, fill=_hl, pct=(_i == 7))   # R-0908-1
    row += 1
put(ws2, row, 1, '判讀：92卷紗／94染色／96打束頭／98特殊加工 四碼由 Amber 2026-09-04 逐碼裁定入冊（R-0904-2），'
                 '本輪起「待確認」歸零；98 之具體加工類型見 1.主分析「今日站別」欄之子代碼。'
                 '🟥＝筆數≥30 且 DELAY率≥30% 之站別 / Nền đỏ: công đoạn có ≥30 đơn và tỷ lệ DELAY ≥30%',
    wrap=True)
row += 1
row += 1
TAB_COUNTS['2.統計'] = row


# ---------- 2b.產品別準交率 ----------
ws2b = wb.create_sheet('2b.產品別準交率')
row = 1
put(ws2b, row, 1, '★ 產品別（料號）準交率 — 前染 NT / 後染 NS 分開計算 ｜ 口徑內部從嚴 L2'
                  ' / OTD theo mã SP, tách Nhuộm Trước (NT) và Nhuộm Sau (NS)', bold=True, wrap=True)
row += 1
put(ws2b, row, 1, '🟨 每群準交率最低前 3 名標黃底（分母 ≥%d 才列名，避免小樣本失真）'
                  ' / 3 mã thấp nhất mỗi nhóm được tô vàng (mẫu số ≥%d)' % (OTD_MIN_N, OTD_MIN_N), wrap=True)
row += 1
_H2B = ['分群 / Nhóm', '料號 / Mã SP', '代表品名 / Tên SP', 'NT/NS', '筆數 / Số nét',
        'OTD分母 / Mẫu số', '準時 / Đúng hạn', '準交率 / OTD', '未交數量 / SL chưa giao',
        '有DC比例 / Tỷ lệ DC', '保留比例 / Tỷ lệ BL', '主要客戶 / KH chính', '標記 / Đánh dấu']
for _i, _h in enumerate(_H2B, 1):
    put(ws2b, row, _i, _h, fill=F_HDR, bold=True, wrap=True)
row += 1
_pc = lambda v: ('—' if v is None else round(v * 100, 1))
PROD_LOW = {}
for _grp, _tag in (('NT', '前染 NT / Nhuộm Trước'), ('NS', '後染 NS / Nhuộm Sau'),
                   ('', '未分類 / Chưa phân loại')):
    _rows = [a for a in ANA if not a['is89'] and (a['ntns'] or '') == _grp]
    if not _rows:
        continue
    _by = defaultdict(list)
    for a in _rows:
        _by[a['mat']].append(a)
    _stat = []
    for _m, _g in _by.items():
        _d, _num, _rt = otd_rate([(a['otd'][0], a['otd'][1]) for a in _g])
        _stat.append({'mat': _m, 'n': len(_g), 'den': _d, 'num': _num, 'otd': _rt,
                      'undel': round(sum(a['undel'] for a in _g), 1),
                      'dc': sum(1 for a in _g if a['has_dc']) / len(_g),
                      'kp': sum(1 for a in _g if a['kept']) / len(_g),
                      'pname': Counter(a['pname'] for a in _g).most_common(1)[0][0],
                      'cust': '/'.join(k for k, _ in Counter(
                          (a['sc'] or a['code']) for a in _g).most_common(2))})
    _rank = sorted([s for s in _stat if s['den'] >= OTD_MIN_N], key=lambda s: (s['otd'], -s['n']))
    _low3 = {s['mat'] for s in _rank[:3]}
    if _grp:
        PROD_LOW[_grp] = _rank[:3]
    for s in sorted(_stat, key=lambda s: (s['otd'] is None, s['otd'] if s['otd'] is not None else 9, -s['n'])):
        _hit = s['mat'] in _low3
        _f = F_YEL if _hit else None
        _mark = ('🟨最低前3·優先檢討 / Top3 thấp nhất' if _hit
                 else ('小樣本(分母<%d)·僅供參考 / Mẫu nhỏ' % OTD_MIN_N if s['den'] < OTD_MIN_N else ''))
        for _i, _v in enumerate([_tag, s['mat'], s['pname'], (_grp or '(未分類)'), s['n'], s['den'],
                                 s['num'], _pc(s['otd']), s['undel'], _pc(s['dc']), _pc(s['kp']),
                                 s['cust'], _mark], 1):
            put(ws2b, row, _i, _v, fill=_f, bold=_hit, pct=(_i in (8, 10, 11)))   # R-0908-1
        row += 1
    row += 1

row += 1
put(ws2b, row, 1, '★ 準交率最低 30 名「品名」— 是否需額外備料判定'
                  ' / Top 30 tên SP có OTD thấp nhất — có cần chuẩn bị thêm NL không', bold=True, wrap=True)
row += 1
put(ws2b, row, 1, '判定規則（系統建議·最終由業務裁定）／Quy tắc đề xuất, NV quyết định cuối:'
                  ' ①OTD<50% 且 未交量>0 且 保留比例<50% → 🔴建議加備料'
                  ' ②OTD<70% 且 有DC比例<50% → 🟠建議先補掛預告(89)'
                  ' ③其餘 → ⚪先查原因不加料（避免呆料）', wrap=True)
row += 1
_H30 = ['# / STT', '品名 / Tên SP', '料號 / Mã SP', 'NT/NS(前後染)', '筆數 / Số nét',
        'OTD分母 / Mẫu số', '準時 / Đúng hạn', '準交率 / OTD', '未交數量 / SL chưa giao',
        '單位 / ĐV', '有DC比例 / Tỷ lệ DC', '保留比例 / Tỷ lệ BL', '主要客戶 / KH chính',
        '備料判定(系統建議) / Đề xuất chuẩn bị NL', '業務確認 / NV xác nhận']
for _i, _h in enumerate(_H30, 1):
    put(ws2b, row, _i, _h, fill=F_HDR, bold=True, wrap=True)
row += 1
_byn = defaultdict(list)
for a in ANA:
    if not a['is89']:
        _byn[a['pname']].append(a)
_ns = []
for _p, _g in _byn.items():
    _d, _num, _rt = otd_rate([(a['otd'][0], a['otd'][1]) for a in _g])
    if _d < OTD_MIN_N:
        continue
    _u = round(sum(a['undel'] for a in _g), 1)
    _dcr = sum(1 for a in _g if a['has_dc']) / len(_g)
    _kpr = sum(1 for a in _g if a['kept']) / len(_g)
    if _rt < 0.5 and _u > 0 and _kpr < 0.5:
        _v = '🔴建議加備料 / Nên chuẩn bị thêm NL'
    elif _rt < 0.7 and _dcr < 0.5:
        _v = '🟠建議先補掛預告89 / Nên gắn DC trước'
    else:
        _v = '⚪先查原因不加料 / Tìm nguyên nhân trước, chưa thêm NL'
    _ns.append({'p': _p, 'mat': Counter(a['mat'] for a in _g).most_common(1)[0][0],
                'ntns': Counter((a['ntns'] or '(未分類)') for a in _g).most_common(1)[0][0],
                'n': len(_g), 'den': _d, 'num': _num, 'otd': _rt, 'u': _u,
                'unit': Counter(a['unit'] for a in _g).most_common(1)[0][0],
                'dc': _dcr, 'kp': _kpr, 'verdict': _v,
                'cust': '/'.join(k for k, _ in Counter((a['sc'] or a['code']) for a in _g).most_common(2))})
_ns.sort(key=lambda s: (s['otd'], -s['u']))
TOP30 = _ns[:30]
for _i, s in enumerate(TOP30, 1):
    _f = F_YEL if _i <= 3 else None
    for _j, _v in enumerate([_i, s['p'], s['mat'], s['ntns'], s['n'], s['den'], s['num'],
                             _pc(s['otd']), s['u'], s['unit'], _pc(s['dc']), _pc(s['kp']),
                             s['cust'], s['verdict'], ''], 1):
        put(ws2b, row, _j, _v, fill=(F_YEL if (_f and _j <= 14) else (F_YEL if _j == 15 else None)),
            bold=(_i <= 3), pct=(_j in (8, 11, 12)))   # R-0908-1
    row += 1
for _c, _w in zip('ABCDEFGHIJKLMNO', [22, 34, 14, 16, 9, 11, 11, 11, 14, 8, 13, 13, 20, 34, 16]):
    ws2b.column_dimensions[_c].width = _w
ws2b.freeze_panes = 'A5'
TAB_COUNTS['2b.產品別準交率'] = row - 1
print('2b 產品別準交率：NT/NS 分群%d｜品名Top30=%d｜全體OTD=%s'
      % (len(PROD_LOW), len(TOP30),
         ('—' if CAT_OTD.get('全體', {}).get('otd') is None
          else '%.1f%%' % (CAT_OTD['全體']['otd'] * 100))))

# ---------- 3.樣品量產預告 ----------
ws3 = wb.create_sheet('3.樣品量產預告')
row = 1
put(ws3, row, 1, '樣品 / 量產 等級對比（89 預告依 R-v522-2 不列異常，異常管理走 4b/6/6b/觀察）', bold=True)
row += 1
put(ws3, row, 1, '類別 / Loại', fill=F_HDR, bold=True)
for j, lv in enumerate(('DELAY', 'WARNING', 'POTENTIAL', 'OK'), 2):
    put(ws3, row, j, lv, fill=F_HDR, bold=True)
row += 1
for name, pred in (('樣品(85/86/87)', lambda a: a['cat'] in ('85', '86', '87')),
                   ('量產(88)', lambda a: a['cat'] == '88')):
    put(ws3, row, 1, name)
    for j, lv in enumerate(('DELAY', 'WARNING', 'POTENTIAL', 'OK'), 2):
        put(ws3, row, j, sum(1 for a in ANA if pred(a) and a['level'] == lv))
    row += 1
put(ws3, row, 1, '預告(89)')
put(ws3, row, 2, '—(R-v522-2 不列異常·%d 筆 / không tính bất thường)' % n89)
row += 2
put(ws3, row, 1, '測試結果分佈（active 非89）/ Phân bố KQTN', bold=True)
row += 1
tc = Counter(dnz(a['row'][32]).upper() or '(空)' for a in ANA if not a['is89'])
for k, v in tc.most_common():
    put(ws3, row, 1, k)
    put(ws3, row, 2, v)
    row += 1
row += 1
put(ws3, row, 1, 'NT/NS × 等級（v%d 採認態·%d 鍵；未分類為新見料號·待人工判定）' % (NTNS_VER, len(NTNS) + 2), bold=True)
row += 1
nn = Counter((a['ntns'] or '未分類(待人工判定)', a['level']) for a in ANA if not a['is89'])
groups = sorted({k[0] for k in nn})
put(ws3, row, 1, '分組 / Nhóm', fill=F_HDR, bold=True)
for j, lv in enumerate(('DELAY', 'WARNING', 'POTENTIAL', 'OK'), 2):
    put(ws3, row, j, lv, fill=F_HDR, bold=True)
row += 1
for g in groups:
    put(ws3, row, 1, g)
    for j, lv in enumerate(('DELAY', 'WARNING', 'POTENTIAL', 'OK'), 2):
        put(ws3, row, j, nn.get((g, lv), 0))
    row += 1
row += 1
put(ws3, row, 1, '各業務 DELAY/WARNING（排除89）/ Theo NV', bold=True)
row += 1
nvw = Counter((a['nv'] or '(空)', a['level']) for a in ANA if not a['is89'])
put(ws3, row, 1, '業務 / Nghiệp vụ', fill=F_HDR, bold=True)
put(ws3, row, 2, 'DELAY', fill=F_HDR, bold=True)
put(ws3, row, 3, 'WARNING', fill=F_HDR, bold=True)
row += 1
for nv in sorted({a['nv'] or '(空)' for a in ANA if not a['is89']}):
    put(ws3, row, 1, nv)
    put(ws3, row, 2, nvw.get((nv, 'DELAY'), 0))
    put(ws3, row, 3, nvw.get((nv, 'WARNING'), 0))
    row += 1
row += 1
put(ws3, row, 1, '越南職場行動：以流程缺口框定、經正式管道回饋、不指向個人 / Hành động: tập trung lỗ hổng quy trình, phản hồi qua kênh chính thức, không quy trách nhiệm cá nhân', wrap=True)
row += 1
TAB_COUNTS['3.樣品量產預告'] = row

# ---------- 4 / 4s / 4w ----------
PLACE_TXT_4S = ('⛔ 系統資料待補·非異常 ｜ Dữ liệu hệ thống chờ bổ sung, không tính lỗi trợ lý ｜ '
                '4s 佔位依據=R-v527-1（Amber 0715·覆蓋率基準·僅轄 4s）：89DB 累積起始 %s，現存 active 89 下單日覆蓋 %d/%d，'
                '全數覆蓋（或 12 支歷史區間檔齊備·現 %d/12）即自動解除；佔位期間不派工、不列業助追蹤'
                % (COV['start'], COV['covered'], COV['total'], PRE['interval_89_files']))

ws4 = wb.create_sheet('4.應掛未掛')
ws4.sheet_properties.tabColor = 'FFFF0000'
H4 = ['群組#', '列別 ①正單/②應掛89', '客戶代碼 / Mã KH', '客戶簡稱 / Tên tắt KH', '訂單號碼 / Mã đơn',
      '#序號 / STT', '類別 / Loại', '料號 / Mã SP', '色號 / Màu', '寬度 / QC', '型號 / Độ dài',
      '數量 / SL', '單位 / ĐV', UNDEL_HDR, '未交量判定 / Phán định SL chưa giao',
      '同89合計檢查(R-0916-29) / Kiểm tra tổng cùng 89',
      '下單日 / Ngày xuống đơn',
      '已掛89(DC) / Đã gắn 89(DC)', '保留量 / SL bảo lưu', '業務 / Nghiệp vụ', '助理 / Trợ lý'] + BF_HDRS

# ══ R-0916-29（Amber 林彥博 2026-09-16「T1-K 只加一個提示欄」·純呈現層）同 89 跨群合計檢查 ══
# 成因：R-v528-3 係**逐群**比對（單張正式單 未交 vs 配對 89 未交），不做同一張 89 的跨群合計扣抵。
#   0916 T1 實證：GOLDEN VIC 5 群共用 89 8926077696，單張皆「可整單取用」成立，
#   但 5 張合計未交 ＞ 該 89 未交 —— 現行判定看不到此缺口。
# 處置（Amber 明示「只加一個提示欄」）：**僅新增提示欄，判定式一行未動**；
#   S4 之群數、列數、豁免計數與所有其他分頁數字必須與 v582 逐格相同。
_s4_by89 = defaultdict(lambda: {'n': 0, 'sum': 0.0, 'u89': 0.0, 'unit': ''})
for _a4, _x4, _f4, _d4, _u4 in S4:
    _k89 = (_x4['order'], dnz(_x4['row'][3]))
    _e = _s4_by89[_k89]
    _e['n'] += 1
    _e['sum'] += fnum(undel(_a4['row']))
    _e['u89'] = fnum(undel(_x4['row']))
    _e['unit'] = dnz(_x4['row'][16])


def s4_group_hint(x89):
    """同一張 89（單號＋序號）被幾個群共用、合計未交是否超過該 89 之未交量。純提示·不參與判定。"""
    e = _s4_by89[(x89['order'], dnz(x89['row'][3]))]
    if e['n'] <= 1:
        return '單群·無合計議題 / Chỉ 1 nhóm, không có vấn đề tổng'
    over = e['sum'] > e['u89']
    return ('%s 同89共 %d 群·正式單合計未交 %s%s vs 本89未交 %s%s / %d nhóm dùng chung 89: tổng %s vs %s'
            % ('⚠️合計超額' if over else '✅合計仍足', e['n'],
               round(e['sum'], 2), e['unit'], round(e['u89'], 2), e['unit'],
               e['n'], round(e['sum'], 2), round(e['u89'], 2)))
for j4, h4 in enumerate(H4, 1):
    put(ws4, 1, j4, h4, fill=F_HDR, bold=True)
ri4 = 2
g4 = 0
V4_TXT = {'full': '✅未交>=正式單·可整單取用 → 異常成立 / Đủ SL, lấy được cả đơn',
          'partial': ('🟠200<=未交<正式單·無法整單取用但剩餘過多 → 人工判定是否先用完再生產 / '
                      'Không đủ cả đơn nhưng tồn nhiều: cần XN dùng hết trước khi SX'),
          'unit_na': ''}
for a, x89, fd4, d89_4, u4 in S4:
    g4 += 1
    for tag, xx in (('①正式單', a), ('②應掛89', x89)):
        rr = xx['row']
        _v4 = ((V4_TXT.get(u4['v'], '') + u4['note']) if tag == '②應掛89'
               else '（對照基準：正式訂單數量 %s%s）/ Cơ sở đối chiếu' % (fnum(rr[15]), dnz(rr[16])))
        vals4 = [g4, tag, xx['code'], xx['sc'] or xx['code'], xx['order'], dnz(rr[3]), xx['cat'],
                 dnz(rr[11]), dnz(rr[12]), fnum(rr[13]), dnz(rr[14]), fnum(rr[15]), dnz(rr[16]),
                 undel(rr), _v4, s4_group_hint(x89),
                 dstr(rr[4]), '—', 0, xx['nv'], xx['tl']]
        for j4, v4 in enumerate(vals4, 1):
            put(ws4, ri4, j4, v4, txt=(j4 == 3))
        if tag == '①正式單':
            prog4 = ('🔴應掛未掛(R-v528-3)·正單晚於89且DC未掛且保留=0·請確認掛DC並回填 / '
                     'Đơn chính sau 89, chưa gắn DC & bảo lưu=0: vui lòng xác nhận gắn DC và báo cáo')
        else:
            prog4 = '—配對89(參照列·同群組驗證用) / Dòng 89 đối chiếu trong nhóm'
        rec4b = ORDERS.get(a['order'])
        bf_cells(ws4, ri4, len(vals4) + 1, prog4,
                 dnz(rec4b.get('raw_reason')) if (tag == '①正式單' and rec4b) else '',
                 dnz(rec4b.get('backfill_date')) if (tag == '①正式單' and rec4b) else '')
        ri4 += 1
if not S4:
    if POP89_ABSENT:
        put(ws4, 2, 1, HALT563, bold=True, wrap=True)
    else:
        put(ws4, 2, 1, '本輪現檔判定無應掛未掛異常（R-v528-3·同日=SOP、89晚=正常、已掛DC/保留>0/白名單/DGT 豁免） / '
            'Không có bất thường trong kỳ này', wrap=True)
ws4.freeze_panes = 'A2'
ws4.auto_filter.ref = f'A1:{get_column_letter(len(H4))}{max(ri4-1,2)}'
TAB_COUNTS['4.應掛未掛'] = ri4 - 2

# ══ R-0916-36（Amber 林彥博 2026-09-16「H2-做」）4s.共用89餘量不足 作用態實作 ══
# 定義：**多張正式單掛同一張 89（同料號/色號/寬度/型號），合計未交量 ＞ 該 89 未交量**。
# 前提：R-v527-1 覆蓋率閘門達標（SHEET4_GATE）才作用；未達標維持佔位（不變）。
# 分攤：R-v500-1 FIFO greedy —— 依正式單下單日由早到晚，吃得下就扣、吃不下就標短缺並**繼續看下一張**
#       （不是後面全短缺；與 v500 棒之 unit_fifo() 單元測試同義）。
# 單位：R-0918-8 起同計量類別直接換算、跨類別須同規格實秤資料；不可換算者 → 該群標「需人工判定」，
#       不納入加總、不宣告短缺。
S4S = []
if SHEET4_GATE:
    _fm_by_dc = defaultdict(list)
    for _a in ANA:
        if _a['is89']:
            continue
        _dc = dnz(_a['row'][30])
        if _dc in ('', '0'):
            continue
        _fm_by_dc[_dc].append(_a)
    for _a in ANA:
        if not _a['is89']:
            continue
        _r89 = _a['row']
        _k = (dnz(_r89[11]).upper(), dnz(_r89[12]).upper(), fnum(_r89[13]), dnz(_r89[14]).upper())
        _share = [f for f in _fm_by_dc.get(_a['order'], [])
                  if (dnz(f['row'][11]).upper(), dnz(f['row'][12]).upper(),
                      fnum(f['row'][13]), dnz(f['row'][14]).upper()) == _k]
        if len(_share) < 2:
            continue                      # 單張獨用 → 非「共用」
        _u89 = dnz(_r89[16])
        # R-0918-8：正式單未交量換算至 89 單位；同類直接換算、跨類別須同規格實秤資料，否則標人工判定
        _spec = (dnz(_r89[11]).upper(), fnum(_r89[13]), dnz(_r89[14]).upper())
        for _f in _share:
            _f['_cv'] = conv_qty(undel(_f['row']), dnz(_f['row'][16]), _u89, _spec)
        _mixed = sorted({dnz(f['row'][16]) for f in _share if f['_cv'][0] is None})
        _rem = undel(_r89)
        _need = round(sum(f['_cv'][0] for f in _share if f['_cv'][0] is not None), 3)
        if _mixed:
            _verdict = ('⚠️單位不可換算·需人工判定（89=%s／正式單含 %s·R-0918-8 跨類別無實秤）·不加總不宣告短缺 / '
                        'Đơn vị khác, cần XN thủ công' % (_u89, '、'.join(_mixed)))
        elif _need <= _rem:
            continue                      # 餘量足夠 → 非異常，不列
        else:
            _verdict = ('🔴共用餘量不足·短缺 %s%s（需求 %s ÷ 剩餘 %s）/ Thiếu %s%s'
                        % (round(_need - _rem, 2), _u89, _need, _rem, round(_need - _rem, 2), _u89))
        _share.sort(key=lambda f: (as_date(f['row'][4]) or datetime.date(1900, 1, 1), f['order']))
        S4S.append((_a, _share, _rem, _need, _u89, bool(_mixed), _verdict))

ws4s = wb.create_sheet('4s.共用89餘量不足')
if not SHEET4_GATE:
    put(ws4s, 1, 1, PLACE_TXT_4S, bold=True, wrap=True)
    ws4s.merge_cells('A1:H1')
    put(ws4s, 2, 1, '（佔位列·非異常·不算業助過失 / không tính lỗi trợ lý）', wrap=True)
    ws4s.column_dimensions['A'].width = 120
    TAB_COUNTS['4s.共用89餘量不足'] = 0
else:
    H4S = ['群組# / Nhóm', '列別 ①89/②正式單 / Loại dòng', '客戶代碼 / Mã KH', '客戶簡稱 / Tên tắt KH',
           '品牌·PM / Nhãn·PM', '訂單號碼 / Mã đơn', '#序號 / STT', '類別 / Loại', '料號 / Mã SP',
           '色號 / Màu', '寬度 / QC', '型號 / Độ dài', '下單日 / Ngày xuống đơn', UNDEL_HDR, '單位 / ĐV',
           '共用單數 / Số đơn dùng chung', '需求合計 / Tổng nhu cầu', '89剩餘 / SL còn 89',
           '短缺量 / Lượng thiếu', 'FIFO判定 / Phán định FIFO', '業務 / Nghiệp vụ', '助理 / Trợ lý'] + BF_HDRS
    # ★ 作用態橫幅**不得**出現「待補」或 R-v527-1 字樣 —— v500 棒以該兩字樣判別佔位／作用態分支。
    put(ws4s, 1, 1, ('★ 4s 作用態（R-0916-36·Amber 0916「H2-做」）｜判定＝多張正式單掛同一張 89'
                     '（同料號/色號/寬度/型號）且合計未交 ＞ 89 未交｜分攤＝R-v500-1 FIFO（依下單日·吃不下即跳過續看）｜'
                     '單位依 R-0918-8 換算（同類直換·跨類別須同規格實秤）·不可換算者不加總標人工判定｜覆蓋率閘門已達標：起始 %s·覆蓋 %d/%d｜累積檔：%s'
                     ' / Chế độ hoạt động: nhiều đơn chính dùng chung 1 đơn 89, tổng nhu cầu vượt SL còn lại'
                     % (COV['start'], COV['covered'], COV['total'], ACC_NOTE)), bold=True, wrap=True)
    for _j, _h in enumerate(H4S, 1):
        put(ws4s, 2, _j, _h, fill=F_HDR, bold=True)
    assert '待補' not in dnz(ws4s.cell(1, 1).value) and 'R-v527-1' not in dnz(ws4s.cell(1, 1).value), \
        'R-0916-36 自證：4s 作用態橫幅不得含「待補」或 R-v527-1（否則 v500 棒會誤走佔位分支）'
    _ri = 3
    _g = 0
    for _a89, _share, _rem, _need, _u89, _mix, _vd in S4S:
        _g += 1
        _r89 = _a89['row']
        _short = '' if _mix else round(max(_need - _rem, 0), 2)
        _rows = [('①89', _a89, _rem, '%d' % len(_share), _need, _rem, _short, _vd)]
        _pool = _rem
        for _f in _share:
            _q = undel(_f['row'])
            _qc, _how = _f['_cv']
            if _mix:
                _fv = '⚠️單位不可換算·需人工判定 / Cần XN thủ công'
                _rows.append(('②正式單', _f, _q, '', '', '', '', _fv))
                continue
            _sfxh = ('｜' + _how) if _how else ''
            if _qc <= _pool + 1e-9:
                _pool -= _qc
                _fv = '✅可取用·扣後餘 %s%s / Lấy được, còn %s%s' % (round(_pool, 2), _u89, round(_pool, 2), _sfxh)
            else:
                _fv = '🔴短缺·現有餘量 %s%s 不足 / Thiếu, chỉ còn %s%s' % (round(_pool, 2), _u89, round(_pool, 2), _sfxh)
            _rows.append(('②正式單', _f, _q, '', '', '', '', _fv))
            continue
            if _q <= _pool + 1e-9:
                _pool -= _q
                _fv = '✅可取用·扣後餘 %s%s / Lấy được, còn %s' % (round(_pool, 2), _u89, round(_pool, 2))
            else:
                _fv = '🔴短缺·現有餘量 %s%s 不足 / Thiếu, chỉ còn %s' % (round(_pool, 2), _u89, round(_pool, 2))
            _rows.append(('②正式單', _f, _q, '', '', '', '', _fv))
        for _tag, _x, _q, _n, _nd, _rm, _sh, _fv in _rows:
            _rr = _x['row']
            _vals = [_g, _tag, _x['code'], _x['sc'] or _x['code'],
                     ('%s·%s' % (_x.get('bn', ''), _x.get('pm', ''))).strip('·'),
                     _x['order'], dnz(_rr[3]), _x['cat'], dnz(_rr[11]), dnz(_rr[12]),
                     fnum(_rr[13]), dnz(_rr[14]), dstr(_rr[4]), _q, dnz(_rr[16]),
                     _n, _nd, _rm, _sh, _fv, _x['nv'], _x['tl']]
            for _j, _v in enumerate(_vals, 1):
                put(ws4s, _ri, _j, _v, txt=(_j == 3))
            _rec = ORDERS.get(_x['order'])
            bf_cells(ws4s, _ri, len(_vals) + 1, _fv,
                     dnz(_rec.get('raw_reason')) if _rec else '',
                     dnz(_rec.get('backfill_date')) if _rec else '')
            _ri += 1
    if not S4S:
        put(ws4s, 3, 1, ('本輪無共用89餘量不足（R-0916-36 作用態·已檢視全部 active 89）·非佔位 / '
                         'Không có thiếu 89 dùng chung trong kỳ này'), wrap=True)
    ws4s.freeze_panes = None
    ws4s.auto_filter.ref = 'A2:%s%d' % (get_column_letter(len(H4S)), max(_ri - 1, 3))
    TAB_COUNTS['4s.共用89餘量不足'] = max(_ri - 3, 0)
print('4s（R-0916-36）：%s｜%d 群 / %d 列'
      % ('作用態' if SHEET4_GATE else '佔位態', len(S4S), TAB_COUNTS['4s.共用89餘量不足']))

ws4w = wb.create_sheet('4w.白名單')
put(ws4w, 1, 1, (f"白名單鏡像（R-v537-1·跟隨 columnar 字典迭代·{len(WL4['entries'])} 筆·棘輪≥{WL4.get('ratchet_min','—')}）｜"
                 f"雙鍵豁免：89號 OR 客戶+料號｜本表=每輪隨檔備份 / Bản sao danh sách trắng"), wrap=True)
_h4w = ['89訂單號 / Mã đơn 89', '客戶代碼 / Mã KH', '料號 / Mã SP', '類別 / Loại', '備註 / Ghi chú', '收錄日 / Ngày ghi', '來源版 / Nguồn']
for _j, _hv in enumerate(_h4w, 1):
    put(ws4w, 2, _j, _hv, bold=True)
for _i, _e in enumerate(WL4['entries'], 3):
    for _j, _v in enumerate([_e.get('order', ''), _e.get('cust', ''), _e.get('MA', ''), _e.get('category', ''),
                             _e.get('remark', ''), _e.get('since_date', ''), _e.get('source', '')], 1):
        put(ws4w, _i, _j, _v)
for _c4w in 'ABCDEFG':
    ws4w.column_dimensions[_c4w].width = 18
ws4w.column_dimensions['E'].width = 40
TAB_COUNTS['4w.白名單'] = len(WL4['entries'])

# ---------- 4b ----------
ws4b = wb.create_sheet('4b.正式單×預告庫存')
ws4b.sheet_properties.tabColor = 'FF7030A0'
H4B = ['客戶代碼 / Mã KH', '客戶簡稱 / Tên tắt KH', '品牌·PM / Nhãn·PM', '訂單號碼 / Mã đơn', '#序號 / STT',
       '類別# / Loại#', '料號 / Mã SP', '色號 / Màu', '寬度 / QC', '型號 / Độ dài',
       '訂單數量 / SL đơn', '訂單單位 / ĐV đơn', UNDEL_HDR, '已掛89(DC) / Đã gắn 89(DC)', '保留量 / SL bảo lưu',
       '單位判定 / Phán định ĐV',
       '同單命中數 / Số lần khớp', '業務 / Nghiệp vụ', '助理 / Trợ lý',
       '📦格位號 / Vị trí kho', '📦入庫料號 / Mã SP nhập kho', '📦入庫色號 / Màu nhập kho',
       '📦入庫日 / Ngày nhập kho', '📦可用未保留 / Khả dụng chưa bảo lưu', '📦庫存單位 / ĐV tồn kho'] + BF_HDRS
for j, h in enumerate(H4B, 1):
    put(ws4b, 1, j, h, fill=F_HDR, bold=True)
S4B.sort(key=lambda t: -(order_days(t[0]['row']) or 0))
ri = 2
if INV_ABSENT:
    put(ws4b, 2, 2, '⛔ 本輪庫存檔（DB_M_D.xls）未提供 → 4b 正式單×預告庫存比對「停判」（R-v545-1），'
                    '本頁 0 列＝未比對，非「無異常」；請上傳最新庫存檔後重跑本頁。'
                    ' / Chưa có file tồn kho (DB_M_D.xls) → mục 4b TẠM DỪNG đối chiếu; '
                    '0 dòng ở đây KHÔNG có nghĩa là không có bất thường.',
        fill=F_YEL, bold=True, wrap=True)
    ri = 3
for a, iv, unit_ok, nh in S4B:
    r = a['row']
    rec = ORDERS.get(a['order'])
    prog = '🔴未掛未保留(系統判定)·請確認庫存來源並補掛89或回填原因 / Chưa gắn DC & chưa bảo lưu, vui lòng XN nguồn tồn kho'
    old, old_d = '', ''
    if rec:
        old, old_d = dnz(rec.get('raw_reason')), dnz(rec.get('backfill_date'))
        if dnz(rec.get('status')) == 'PROCESSING':
            prog = '🔧處理中·待結果 / Đang xử lý, chờ kết quả'
    vals = [a['code'], a['sc'] or a['code'], f"{a['bn']}·{a['pm']}".strip('·'), a['order'], dnz(r[3]), a['cat'],
            dnz(r[11]), dnz(r[12]), fnum(r[13]), dnz(r[14]), fnum(r[15]), dnz(r[16]), undel(r),
            '—', fnum(r[23]),
            unit_ok, nh, a['nv'], a['tl'],
            iv['slot'], iv['mat'], iv['color'],
            iv['in'].strftime('%Y/%m/%d') if iv['in'] else '', round(iv['avail'], 2), iv['unit']]
    for j, v in enumerate(vals, 1):
        put(ws4b, ri, j, v, txt=(j == 1))
    bf_cells(ws4b, ri, len(vals) + 1, prog, old, old_d)
    ri += 1
ws4b.freeze_panes = 'A2'
ws4b.auto_filter.ref = f'A1:{get_column_letter(len(H4B))}{max(ri-1,2)}'
TAB_COUNTS['4b.正式單×預告庫存'] = (ri - 3) if INV_ABSENT else (ri - 2)

# ---------- 6 ----------
ws6 = wb.create_sheet('6.預告未保留使用')
ws6.sheet_properties.tabColor = 'FFC00000'
H6 = ['客戶代碼 / Mã KH', '客戶簡稱 / Tên tắt KH', '品牌·PM / Nhãn·PM', '89訂單號 / Mã đơn 89', '#序號 / STT',
      '料號 / Mã SP', '色號 / Màu', '寬度 / QC', '型號 / Độ dài', '89數量 / SL 89', '單位 / ĐV', UNDEL_HDR,
      '完工量 / Nhập kho', '已交 / Đã giao', '保留 / Bảo lưu', '下單日 / Ngày xuống đơn', '帳齡天數 / Số ngày tuổi',
      '分級 / Phân cấp', '生命週期狀態 / Trạng thái vòng đời', '再回填次數 / Số lần báo cáo lại',
      '業務 / Nghiệp vụ', '助理 / Trợ lý'] + BF_HDRS
for j, h in enumerate(H6, 1):
    put(ws6, 1, j, h, fill=F_HDR, bold=True)
S6.sort(key=lambda x: (0 if x.get('arj') else 1,
                       0 if 'FORCE' in x['life'] else (1 if '逾期' in x['life'] else 2), -(x.get('days') or 0)))
ri = 2
for x in S6:
    r = x['row']
    vals = [x['code'], x['sc'] or x['code'], f"{x['bn']}·{x['pm']}".strip('·'), x['order'], dnz(r[3]), dnz(r[11]),
            dnz(r[12]), fnum(r[13]), dnz(r[14]), fnum(r[15]), dnz(r[16]), undel(r), fnum(r[20]), fnum(r[21]),
            fnum(r[23]), dstr(r[4]), x.get('days'), x.get('grade', '—'), x['life'], x.get('refill', 0),
            x['nv'], x['tl']]
    for j, v in enumerate(vals, 1):
        put(ws6, ri, j, v, txt=(j == 1))
    bf_cells(ws6, ri, len(vals) + 1, x['prog'], x.get('old', ''), x.get('old_d', ''))
    ri += 1
ws6.freeze_panes = 'A2'
ws6.auto_filter.ref = f'A1:{get_column_letter(len(H6))}{max(ri-1,2)}'
if POP89_ABSENT:
    put(ws6, 2, 1, HALT563, bold=True, wrap=True)
TAB_COUNTS['6.預告未保留使用'] = ri - 2

# ---------- 6觀察名單 ----------
ws6w = wb.create_sheet('6觀察名單')
H6W = ['客戶簡稱 / Tên tắt KH', '89訂單號 / Mã đơn 89', '#序號 / STT', '料號 / Mã SP', '色號 / Màu',
       '寬度 / QC', '型號 / Độ dài', '數量 / SL', '單位 / ĐV', UNDEL_HDR, '下單日 / Ngày xuống đơn',
       '監控到期 / Hạn theo dõi', '逾期狀態 / Trạng thái theo dõi', '再回填次數 / Số lần báo cáo lại', 'cap',
       '業務 / Nghiệp vụ', '助理 / Trợ lý',
       '異常檢查回報 / Báo cáo kiểm tra', '處置 / Xử lý', '舊回填紀錄(歷史) / Hồ sơ báo cáo cũ']
for j, h in enumerate(H6W, 1):
    put(ws6w, 1, j, h, fill=F_HDR, bold=True)
S6W.sort(key=lambda x: (0 if x.get('wave') else (1 if x['cap'] else 2), x['order']))
ri = 2
for x in S6W:
    r = x['row']
    vals = [x['sc'] or x['code'], x['order'], dnz(r[3]), dnz(r[11]), dnz(r[12]), fnum(r[13]), dnz(r[14]),
            fnum(r[15]), dnz(r[16]), undel(r), dstr(r[4]), x.get('mu', ''), x['over'], x.get('refill', 0),
            x['cap'], x['nv'], x['tl']]
    for j, v in enumerate(vals, 1):
        put(ws6w, ri, j, v, fill=(F_WAVE if x.get('wave') and j == 13 else None))
    put(ws6w, ri, 18, '', fill=F_YEL)
    put(ws6w, ri, 19, x['prog'], fill=F_BLU, wrap=True)
    put(ws6w, ri, 20, (f"[{x.get('old_d','')}] {x.get('old','')}" if x.get('old') else ''), fill=F_GRY, wrap=True)
    ri += 1
ws6w.freeze_panes = 'A2'
ws6w.auto_filter.ref = f'A1:{get_column_letter(len(H6W))}{max(ri-1,2)}'
if POP89_ABSENT:
    put(ws6w, 2, 1, HALT563, bold=True, wrap=True)
TAB_COUNTS['6觀察名單'] = ri - 2

# ---------- 6b ----------
ws6b = wb.create_sheet('6b.重複開單群組')
ws6b.sheet_properties.tabColor = 'FF833C00'
H6B = ['群組ID / Nhóm ID', '群組筆數 / Số dòng nhóm', '客戶代碼 / Mã KH', '客戶簡稱 / Tên tắt KH',
       '89訂單號 / Mã đơn 89', '#序號 / STT', '料號 / Mã SP', '色號 / Màu', '寬度 / QC', '型號 / Độ dài',
       '89數量 / SL 89', '單位 / ĐV', UNDEL_HDR, '完工量 / Nhập kho', '下單日 / Ngày xuống đơn', '已交 / Đã giao',
       '保留 / Bảo lưu', '庫存誤開🟣 / Mở nhầm khi có tồn kho',
       '♻️復檢標記(R-0819-1) / Rà soát lại', '原結案處置 / Xử lý đã đóng trước đó',
       '業務 / Nghiệp vụ', '助理 / Trợ lý'] + BF_HDRS
for j, h in enumerate(H6B, 1):
    put(ws6b, 1, j, h, fill=F_HDR, bold=True)
ri = 2
for gid, gn, x, unc, mis, mis_iv, rck in S6B:
    r = x['row']
    rec = ORDERS.get(x['order'])
    old = dnz(rec.get('raw_reason')) if rec else ''
    old_d = dnz(rec.get('backfill_date')) if rec else ''
    st = dnz(rec.get('status')) if rec else ''
    rawU6 = _norm_raw(old)
    is_252b = bool(RX252.search(rawU6)) and 'KHÔNG CÒN' not in rawU6 and 'KHONG CON' not in rawU6
    if st == 'FORCE':
        prog = FORCE_252_TXT if is_252b else FORCE_TXT
        if rec and rec.get('answer_rejected'):
            prog = ('❌回答被駁回(R-v539-1)·不受理·恆追問三選一｜📌' + dnz(rec.get('directive')) + '｜') + prog
        if rec and rec.get('conflict_flag'):
            prog = '⚔️跨表衝突登錄·FORCE 待Amber終裁(R-v539-3)·' + prog
    elif x['order'] in CAP_SET:
        prog = LOCK_TXT
    elif st == 'PROCESSING':
        prog = '🔧處理中·待結果 / Đang xử lý'
    elif st == 'OPEN':
        _mu6b = eff_window(rec)
        if rec.get('directive'):
            _pfx6b = '❌回答被駁回·重問(R-v539)·不適用信任窗·' if rec.get('answer_rejected') else ''
            prog = (f"{_pfx6b}📌主管提問(R-v529-2)·原文：{dnz(rec.get('directive'))}·請於反黃兩欄作答 / "
                    f"Câu hỏi của quản lý: {dnz(rec.get('directive'))}")
        elif _mu6b and _mu6b < TODAY.isoformat():
            prog = ('⏰觀察到期回歸(R-v515-1)·請回填處置：依證據結案或三選一 / '
                    'Hết hạn theo dõi, quay lại báo cáo')
        elif _mu6b and _mu6b >= TODAY.isoformat():
            prog = (f'👁觀察窗內·期內不重複詢問(R-v529-1)·到期 {_mu6b} 回歸複查 / '
                    f'Trong thời gian theo dõi ({_mu6b}), không hỏi lại')
        else:
            prog = '⚠️回填態待釐清·請回填原因與處置 / Vui lòng báo cáo nguyên nhân & xử lý'
    else:
        prog = '🆕重複開單·請回填原因(依FC合理重複可結案) / Mở trùng DB, vui lòng báo cáo lý do'
    if rck:
        prog = ('♻️結案後復檢(R-0819-1·Amber 轉正·永久)·本單雖已結案但仍掛在進度總表且未消耗(已交=0·保留=0)；'
                '下批備料之「89未交量」若未計入本單即造成重複備料。請確認：①沖抵後續備料 ②XSD刪單 ③移轉。 / '
                'Rà soát lại sau khi đóng: đơn đã đóng nhưng vẫn trên bảng tiến độ & chưa tiêu thụ. '
                'Nếu lô chuẩn bị NVL kế tiếp không trừ đơn này sẽ chuẩn bị trùng.｜') + prog
    mtxt = mis + (f'（{mis_iv["slot"]}·{mis_iv["mat"]}·{mis_iv["color"]}·入庫{mis_iv["in"].strftime("%m/%d") if mis_iv["in"] else ""}·可用{round(mis_iv["avail"],1)}{mis_iv["unit"]}）' if mis_iv else '')
    vals = [gid, gn, x['code'], x['sc'] or x['code'], x['order'], dnz(r[3]), dnz(r[11]), dnz(r[12]), fnum(r[13]),
            dnz(r[14]), fnum(r[15]), dnz(r[16]), undel(r), fnum(r[20]), dstr(r[4]), fnum(r[21]), fnum(r[23]),
            mtxt, rck,
            (f"[{x.get('recheck_d','')}] {x.get('recheck_src','')}｜原回填：{x.get('recheck_raw','')}" if rck else ''),
            x['nv'], x['tl']]
    for j, v in enumerate(vals, 1):
        cell = put(ws6b, ri, j, v, txt=(j == 3))
        if unc and j <= 2:
            cell.fill = F_UNC
    if mtxt:
        ws6b.cell(ri, 18).fill = F_PUR
    bf_cells(ws6b, ri, len(vals) + 1, prog, old, old_d)
    ri += 1
ws6b.freeze_panes = 'A2'
ws6b.auto_filter.ref = f'A1:{get_column_letter(len(H6B))}{max(ri-1,2)}'
if POP89_ABSENT:
    put(ws6b, 2, 1, HALT563, bold=True, wrap=True)
TAB_COUNTS['6b.重複開單群組'] = ri - 2

# ---------- 6c.重複備料曝險（R-0819-1 附屬） ----------
ws6c = wb.create_sheet('6c.重複備料曝險')
ws6c.sheet_properties.tabColor = 'FFFF6600'
put(ws6c, 1, 1, ('★ R-0819-1（Amber 林彥博 2026-08-19 裁-1·2026-08-26 A1 再確認·轉正·永久）重複備料曝險清單 —— '
                 '同一「客戶+料號+色號+寬度+型號」下有 2 張以上「未消耗(已交=0·保留=0)」之 89 預告單時，'
                 '合理需求量至多為其中一張；「可止損量＝合計未交 − 最大單未交」即為重複備料之曝險。'
                 '成因：下一批備料表之「89未交量 / 89 TON KHO TP」欄未計入前批新開之 89 → 重複備料。 / '
                 'Danh sách rủi ro chuẩn bị NVL trùng: khi một quy cách có ≥2 đơn DB 89 chưa tiêu thụ, '
                 'lượng có thể cắt lỗ = tổng SL chưa giao − đơn lớn nhất.'), bold=True, wrap=True)
put(ws6c, 2, 1, ('本輪實證：ADIANA｜67ATT-012｜3PB1309｜寬15 —— 6/24 批備料 2,197Y（89未交欄填 247），'
                 '7/20 批「89未交量」仍填 247、未計入 6/24 已開之 89 → 再備 2,440Y。可止損 2,197Y。'), wrap=True)
# R-0819-1（Amber 0819 追加指示）：各群組之 89 訂單「垂直並列」——一張 89 一列，該規格所有未交完之 89 全列
H6C = ['群組# / Nhóm', '群內序 / STT nhóm', '客戶代碼 / Mã KH', '客戶簡稱 / Tên tắt KH',
       '料號 / Mã SP', '色號 / Màu', '寬度 / QC', '型號 / Độ dài', '單位 / ĐV',
       '群·未消耗89張數 / Số đơn chưa tiêu thụ', '群·合計未交(未消耗) / Tổng chưa giao',
       '群·最大單未交 / Đơn lớn nhất', '⚠️群·可止損量 / Có thể cắt lỗ',
       '89訂單號 / Mã đơn 89', '#序號 / STT', '下單日 / Ngày xuống đơn', '帳齡天 / Tuổi (ngày)',
       '89數量 / SL 89', '完工量 / Nhập kho', '已交 / Đã giao', '保留 / Bảo lưu',
       '未交數量 / SL chưa giao', '消耗狀態 / Trạng thái tiêu thụ', '判定 / Phán định',
       '♻️復檢標記(R-0819-1) / Rà soát lại', '原結案處置 / Xử lý đã đóng trước đó',
       '業務 / Nghiệp vụ', '助理 / Trợ lý'] + BF_HDRS
for j, h in enumerate(H6C, 1):
    put(ws6c, 3, j, h, fill=F_HDR, bold=True, wrap=True)
F_G1 = PatternFill('solid', fgColor='FFEAF1FB')     # 群組交替底色（左側規格區）
F_G2 = PatternFill('solid', fgColor='FFFDF2E9')
F_KEEP = PatternFill('solid', fgColor='FFD9EAD3')   # ✅保留基準
F_CUT = PatternFill('solid', fgColor='FFF4CCCC')    # ⚠️建議止損
F_NA = PatternFill('solid', fgColor='FFF2F2F2')     # ◽已消耗
ri = 4
for _gi, d in enumerate(S6C):
    _gf = F_G1 if _gi % 2 == 0 else F_G2
    _top = ri
    for _k, dd in enumerate(d['dets'], 1):
        gvals = [d['gid'], _k, d['code'], d['sc'], d['mat'], d['color'], d['w'], d['model'], d['unit'],
                 d['n'], d['tot'], d['mx'], d['loss']]
        for j, v in enumerate(gvals, 1):
            put(ws6c, ri, j, v, txt=(j == 3), fill=(F_YEL if j == 13 else _gf),
                bold=(j == 13 and _k == 1))
        _vf = (F_CUT if '建議止損' in dd['verdict'] else
               (F_KEEP if '保留基準' in dd['verdict'] else F_NA))
        dvals = [dd['order'], dd['stt'], dd['date'], dd['age'], dd['qty'], dd['done'],
                 dd['giao'], dd['bl'], dd['und'], dd['state'], dd['verdict'], dd['rck'],
                 dd['rck_src'], dd['nv'], dd['tl']]
        for j, v in enumerate(dvals, 14):
            _c = put(ws6c, ri, j, v, wrap=(j in (23, 24, 26)),
                     fill=(_vf if j in (22, 23, 24) else None))
            if j == 24 and '建議止損' in str(v):
                _c.font = Font(bold=True, color='FFC00000')
            elif j == 24 and '保留基準' in str(v):
                _c.font = Font(bold=True, color='FF006100')
        bf_cells(ws6c, ri, len(gvals) + len(dvals) + 1,
                 ('⚠️重複備料曝險·請三擇一並回填：①後批備料沖抵本量 ②XSD 刪除多餘 89 ③移轉他客戶/報廢。限期為建議值。 / '
                  'Rủi ro chuẩn bị trùng: chọn 1 trong 3 (①trừ vào lô sau ②XSD ③chuyển/hủy)')
                 if '建議止損' in dd['verdict'] else
                 ('—參照列（保留基準或已消耗）·無需處置 / Dòng đối chiếu, không cần xử lý'), '', '')
        ri += 1
    _ = _top   # 群組欄逐列重覆·不合併儲存格（合併會使篩選與外部讀取斷行）
if not S6C:
    put(ws6c, 4, 1, '本輪無重複備料曝險群組（或 89 母體停判） / Không có nhóm rủi ro trong kỳ này', wrap=True)
ws6c.freeze_panes = 'N4'
ws6c.auto_filter.ref = f'A3:{get_column_letter(len(H6C))}{max(ri-1,4)}'
TAB_COUNTS['6c.重複備料曝險'] = sum(d['n_open'] for d in S6C)

# ---------- 7w ----------
ws7 = wb.create_sheet('7w.品牌空白')
H7 = ['客戶代碼 / Mã KH', '客戶簡稱 / Tên tắt KH', '品牌代碼(覆蓋後) / Mã nhãn (sau ghi đè)', '狀態 / Trạng thái']
write_table(ws7, H7, [[c, s or '(清冊無簡稱)', '', '品牌欄空白（覆蓋後仍空）·請確認 / Nhãn trống, vui lòng XN'] for c, s in S7W] or
            [['—', '—', '—', '本輪無品牌空白 / Không có nhãn trống']])
TAB_COUNTS['7w.品牌空白'] = len(S7W)
# R-0916-4（Amber 0916「C5入白名單」）：白名單具名列示於表末 —— 抑制不等於隱藏
if S7W_SUP:
    _r7 = ws7.max_row + 2
    put(ws7, _r7, 1, '★ R-0916-4（Amber 林彥博 2026-09-16「C5入白名單」）已確認無品牌線·不列異常 / '
                     'Đã xác nhận không có dây chuyền nhãn · không tính bất thường')
    for _i, (_c, _s) in enumerate(S7W_SUP, 1):
        _e = SUPPRESS_7W.get(_c, {})
        put(ws7, _r7 + _i, 1, _c)
        put(ws7, _r7 + _i, 2, _s or '(清冊無簡稱)')
        put(ws7, _r7 + _i, 3, '(無品牌碼)')
        put(ws7, _r7 + _i, 4, '✅ 白名單抑制 / Danh sách trắng｜%s' % _e.get('reason', ''))

# ---------- 8.NTNS未分類 ----------
ws8 = wb.create_sheet('8.NTNS未分類')
put(ws8, 1, 1, '★ v%d 採認態：本頁為剩餘未分類料號，待人工判定後回傳·本輪不派工 / '
    'Trạng thái v%d: mã còn lại chờ phân loại thủ công, không phân công đợt này。'
    '（Amber 留白待判·維持留白：%s）' % (NTNS_VER, NTNS_VER, '／'.join(sorted(PENDING_BLANK))),
    bold=True, wrap=True)
ws8.merge_cells(f'A1:{get_column_letter(9)}1')
H8 = ['料號 / Mã SP', '色號(一組) / Màu (một nhóm)', '客戶代碼 / Mã KH', '客戶簡稱 / Tên tắt KH',
      '業務 / Nghiệp vụ', 'NT/NS判定(人工填) / Phân loại NT-NS (điền tay)', '備註 / Ghi chú']
for j, h in enumerate(H8, 1):
    put(ws8, 2, j, h, fill=F_HDR, bold=True)
ri = 3
for m, (col, code8, sc, nv) in S8:
    note = 'Amber 留白待判·勿臆測 / Amber để trống, không suy đoán' if m in PENDING_MATS else '新見·待人工判定 / Mới, chờ phân loại'
    for j, v in enumerate([m, col, code8, sc, nv, '', note], 1):
        put(ws8, ri, j, v, txt=(j == 3))
    ri += 1
ws8.freeze_panes = 'A3'
TAB_COUNTS['8.NTNS未分類'] = ri - 3

# ---------- 9.已結案移除 ----------
ws9 = wb.create_sheet('9.已結案移除')
H9 = ['來源表 / Bảng nguồn', '狀態 / Trạng thái', '客戶代碼 / Mã KH', '客戶簡稱 / Tên tắt KH', '訂單號 / Mã đơn',
      '#序號 / STT', '料號 / Mã SP', '色號 / Màu', UNDEL_HDR,
      '結案處置(字典) / Xử lý kết án', '回填日 / Ngày báo cáo',
      '業務 / Nghiệp vụ', '助理 / Trợ lý']
rows9 = []
seen9 = set()
for a, src, st, reason, bdate in S9:
    k = (a['order'], dnz(a['row'][3]), src)
    if k in seen9:
        continue
    seen9.add(k)
    rec = ORDERS.get(a['order']) or {}
    rows9.append([src, st, a['code'], a['sc'] or a['code'], a['order'], dnz(a['row'][3]), dnz(a['row'][11]),
                  dnz(a['row'][12]), undel(a['row']),
                  dnz(rec.get('disp_zh')) or reason, bdate, a['nv'], a['tl']])
write_table(ws9, H9, rows9)
if POP89_ABSENT:
    put(ws9, 2, 1, HALT563, bold=True, wrap=True)
TAB_COUNTS['9.已結案移除'] = len(rows9)

# ---------- 分類彙總 ----------
wsc = wb.create_sheet('分類彙總')
rows_c = [
    ['Sheet6 合計', len(S6)], ['  ⚠️逾期回歸', sum(1 for x in S6 if '逾期' in x['life'])],
    ['  ⛔FORCE(死預告/R-v525-2)', sum(1 for x in S6 if 'FORCE' in x['life'])],
    ['  🔧處理中', sum(1 for x in S6 if '處理中' in x['life'])],
    ['  🆕新列', sum(1 for x in S6 if '新' in x['life'])],
    ['6觀察 合計', len(S6W)], ['  🔒cap鎖定(禁三進)', sum(1 for x in S6W if x['cap'])],
    ['  👁監控中', sum(1 for x in S6W if not x['cap'])],
    [f'  ⏰{WAVE_MMDD}到期潮(明日·R-v515-1)', n_wave],
    ['6b 群組/列（R-v515-1 過濾後實值）', f'{gid_n}群 / {len(S6B)}列'],
    ['  R-v515-1 觀察中成員自6b移除', n_6b_obs_removed],
    ['♻️R-0819-1 結案後復檢回列（6b）', f'{len(S6B_RECHECK)} 列（家族【預告增量結案】{sum(1 for x in S6B_RECHECK if x.get("recheck_fam"))}／自6觀察回列 {n_6b_obs_pulled_back}）'],
    ['6c 重複備料曝險群組', f'{len(S6C)} 群｜可止損合計 {round(sum(d["loss"] for d in S6C),1)}'],
    ['9.已結案移除', len(rows9)],
    ['4b 未掛未保留', TAB_COUNTS['4b.正式單×預告庫存']],
    ['4.應掛未掛（R-v528-3 現檔判定）', f'{len(S4)}群 / {len(S4)*2}列'],
    ['4s 共用89餘量', f'R-v527-1 佔位（覆蓋 {COV["covered"]}/{COV["total"]}·非異常）'],
    ['Sheet8', f'{len(S8)}（待判·不派工）'],
]
write_table(wsc, ['項目 / Mục', '數值 / Giá trị'], rows_c)
TAB_COUNTS['分類彙總'] = len(rows_c)

# ---------- 派工清單 ----------
wsd = wb.create_sheet('派工清單')
HD = ['類別 / Loại', '來源 / Nguồn', '客戶代碼 / Mã KH', '客戶簡稱 / Tên tắt KH', '訂單號 / Mã đơn',
      '#序號 / STT', '料號 / Mã SP', '色號 / Màu', '系統判定 / Phán định hệ thống', '限期(建議) / Hạn (đề xuất)',
      '業務 / Nghiệp vụ', '助理 / Trợ lý', UNDEL_HDR]
UND_IDX = {(a['order'], dnz(a['row'][3])): undel(a['row']) for a in ANA}
rows_d = []
for x in S6:
    if 'FORCE' in x['life']:
        rows_d.append(['強制', '6', x['code'], x['sc'] or x['code'], x['order'], dnz(x['row'][3]), dnz(x['row'][11]),
                       dnz(x['row'][12]), '⛔FORCE·限期三選一', DUE_FORCE, x['nv'], x['tl']])
# R-0820-1：觀察到期落回者改列「強制」（舊行為為留在觀察名單之「預警」）
for x in S6:
    if x['life'] == '⏰到期回歸':
        rows_d.append(['強制', '6', x['code'], x['sc'] or x['code'], x['order'], dnz(x['row'][3]), dnz(x['row'][11]),
                       dnz(x['row'][12]), '⏰觀察到期回歸(R-0820-1)·有單→結案；無單→移轉/報廢二選一',
                       DUE_FORCE, x['nv'], x['tl']])
for x in S6W:
    if x['cap']:
        rows_d.append(['強制', '6觀察', x['code'], x['sc'] or x['code'], x['order'], dnz(x['row'][3]), dnz(x['row'][11]),
                       dnz(x['row'][12]), '🔒cap鎖定·限期三選一·禁三進', DUE_FORCE, x['nv'], x['tl']])
for x in S6W:
    if x.get('wave'):
        rows_d.append(['預警', '6觀察', x['code'], x['sc'] or x['code'], x['order'], dnz(x['row'][3]), dnz(x['row'][11]),
                       dnz(x['row'][12]), f'⏰{WAVE_MMDD}到期潮·今日預處置：有單→結案；無單→移轉/報廢', DUE_FORCE, x['nv'], x['tl']])
for x in S6:
    if 'FORCE' not in x['life'] and '處理中' not in x['life'] and x['life'] != '⏰到期回歸':
        rows_d.append(['常規', '6', x['code'], x['sc'] or x['code'], x['order'], dnz(x['row'][3]), dnz(x['row'][11]),
                       dnz(x['row'][12]), x['life'] + '·請回填', DUE_NORM, x['nv'], x['tl']])
for a, x89, fd4, d89_4, u4 in S4:
    _sfx = ('·🟠未交%s<正式單%s(>=200)·先判定是否先用完再生產(R-v561-2)' % (u4['und'], u4['qf'])
            if u4['v'] == 'partial' else ('·⚠️單位待裁決(R-v561-2)' if u4['v'] == 'unit_na' else ''))
    rows_d.append(['常規', '4', a['code'], a['sc'] or a['code'], a['order'], dnz(a['row'][3]), dnz(a['row'][11]),
                   dnz(a['row'][12]), f'🔴應掛未掛(R-v528-3)·配對89:{x89["order"]}·請確認DC/回填{_sfx}',
                   DUE_NORM, a['nv'], a['tl']])
seen_line = set()
for a, iv, u, nh in S4B:
    k = (a['order'], dnz(a['row'][3]))
    if k in seen_line:
        continue
    seen_line.add(k)
    rows_d.append(['常規', '4b', a['code'], a['sc'] or a['code'], a['order'], dnz(a['row'][3]), dnz(a['row'][11]),
                   dnz(a['row'][12]), '🔴未掛未保留·請確認/回填', DUE_NORM, a['nv'], a['tl']])
for gid, gn, x, unc, mis, mis_iv, rck in S6B:
    if unc:
        rec = ORDERS.get(x['order'])
        st = dnz(rec.get('status')) if rec else ''
        if st in ('FORCE',) or x['order'] in CAP_SET:
            continue
        _lz = LOSS_BY_ORDER.get(x['order'], 0)
        _t6b = ('♻️結案後復檢(R-0819-1)·重複備料風險·請確認沖抵/XSD/移轉' if rck else '重複開單·請回填原因')
        if _lz:
            _t6b += f'｜本群可止損 {_lz} {dnz(x["row"][16])}'
        rows_d.append([('強制' if rck else '常規'), '6b', x['code'], x['sc'] or x['code'], x['order'],
                       dnz(x['row'][3]), dnz(x['row'][11]), dnz(x['row'][12]), _t6b,
                       (DUE_FORCE if rck else DUE_NORM), x['nv'], x['tl']])
# ---- R-0819-8（Amber 林彥博 2026-08-19「裁-5 開XSD沖銷」）裁決待辦入派工 ----
# 立意：Amber 對特定單之直接指示（如開 XSD 沖銷系統殘量），可能落在所有分頁之外
#   （例：8925124459 已交>0 → 不進 Sheet6 候選；PROCESSING → 不進 6b 復檢）→ 若不另立通道即無人執行。
# 落地：字典 orders 內帶 pending_action 且 status != DONE 者，一律以「強制」列入派工清單。
_ANA_BY_ORDER = {a['order']: a for a in ANA}
n_pa = 0
for _oid, _rec in ORDERS.items():
    _pa = _rec.get('pending_action')
    if not _pa or dnz(_pa.get('status')).upper() == 'DONE':
        continue
    _a = _ANA_BY_ORDER.get(dnz(_oid).upper())
    _code = _a['code'] if _a else dnz(_pa.get('cust'))
    _sc = (_a['sc'] or _code) if _a else dnz(_pa.get('sc'))
    _stt = dnz(_a['row'][3]) if _a else ''
    _mat = dnz(_a['row'][11]) if _a else dnz(_pa.get('mat'))
    _col = dnz(_a['row'][12]) if _a else dnz(_pa.get('color'))
    _nv = _a['nv'] if _a else dnz(_pa.get('owner_nv'))
    _tl = _a['tl'] if _a else dnz(_pa.get('owner_tl'))
    rows_d.append(['強制', '裁決', _code, _sc, dnz(_oid), _stt, _mat, _col,
                   '⚖️Amber 裁示(%s)·%s·%s / %s' % (dnz(_pa.get('rule')), dnz(_pa.get('type')),
                                                     dnz(_pa.get('desc')), dnz(_pa.get('desc_vi'))),
                   DUE_FORCE, _nv, _tl])
    n_pa += 1
if n_pa:
    print('R-0819-8 裁決待辦：%d 筆入派工（強制）' % n_pa)

rows_d = [r0 + [UND_IDX.get((r0[4], dnz(r0[5])), '')] for r0 in rows_d]
write_table(wsd, HD, rows_d)
n_force = sum(1 for r0 in rows_d if r0[0] == '強制')
n_warn_d = sum(1 for r0 in rows_d if r0[0] == '預警')
put(wsd, len(rows_d) + 3, 1,
    f'強制 {n_force}／預警(⏰{WAVE_MMDD}潮) {n_warn_d}／常規 {len(rows_d)-n_force-n_warn_d}｜限期為建議值·非承諾｜'
    f'異常=流程缺口·不指向個人 / Hạn chót chỉ là đề xuất; bất thường = lỗ hổng quy trình', wrap=True)
TAB_COUNTS['派工清單'] = len(rows_d)

# ---------- 收尾 ----------
# ══ R-0904-3（Amber 林彥博 2026-09-04·轉正·永久）分頁順序：須人工回填者一律置前 ══
# amber_ruling：「所有須人工回填的 Sheets 請一律放在最前面，不須回填的 Sheets 向後放」
# 判定準則（機械式·非主觀）：分頁表頭含回填欄（異常原因檢查／處理方式和結果／憑證單號／處理進度）
#   或含人工填欄（NT/NS判定(人工填)、品牌欄請確認）者 → 回填區。
# 0.說明 為封面/圖例（非資料頁）續置首位；派工清單為回填區之指派入口，緊接回填區之後。
TABS_COVER = ['0.說明']
TABS_FILL = ['4.應掛未掛', '4b.正式單×預告庫存', '6.預告未保留使用', '6b.重複開單群組',
             '6c.重複備料曝險', '7w.品牌空白', '8.NTNS未分類']          # 🟥 須人工回填
TABS_BRIDGE = ['派工清單']                                              # 🟧 指派入口
TABS_READ = ['1.主分析', '2.統計', '2b.產品別準交率', '3.樣品量產預告', '4w.白名單',
             '4s.共用89餘量不足', '6觀察名單', '9.已結案移除', '分類彙總']   # 🟦 唯讀分析
ORDER_TABS = TABS_COVER + TABS_FILL + TABS_BRIDGE + TABS_READ
_ALL_TABS = set(TABS_COVER) | set(TABS_FILL) | set(TABS_BRIDGE) | set(TABS_READ)
assert _ALL_TABS == set(TAB_COUNTS), (
    'R-0904-3 FAIL：分頁分組未涵蓋全部分頁 差=%s' % (_ALL_TABS ^ set(TAB_COUNTS)))
for _t in TABS_FILL:
    wb[_t].sheet_properties.tabColor = 'FFC00000'    # 紅＝待回填
for _t in TABS_BRIDGE:
    wb[_t].sheet_properties.tabColor = 'FFED7D31'    # 橘＝指派
for _t in TABS_READ:
    wb[_t].sheet_properties.tabColor = 'FF4472C4'    # 藍＝唯讀分析
wb['0.說明'].sheet_properties.tabColor = 'FF7F7F7F'  # 灰＝封面
wb._sheets = [wb[t] for t in ORDER_TABS]
for t in ORDER_TABS:
    autowidth(wb[t])
TAB_VI = {'0.說明': 'Giải thích', '1.主分析': 'Phân tích chính', '2.統計': 'Thống kê', '2b.產品別準交率': 'OTD theo SP', '3.樣品量產預告': 'Mẫu ra sản xuất', '4.應掛未掛': 'Chưa gắn 89', '4w.白名單': 'Danh sách trắng', '4s.共用89餘量不足': 'Thiếu 89 chung', '4b.正式單×預告庫存': 'Đơn CT×tồn DB', '6.預告未保留使用': 'DB chưa giữ dùng', '6觀察名單': 'DS theo dõi', '6b.重複開單群組': 'Nhóm đơn trùng', '6c.重複備料曝險': 'Rủi ro NVL trùng', '7w.品牌空白': 'Brand trống', '8.NTNS未分類': 'Chưa phân loại', '9.已結案移除': 'Đã đóng gỡ bỏ', '分類彙總': 'Tổng hợp phân loại', '派工清單': 'DS điều phối'}
for _zh, _vi in TAB_VI.items():
    if _zh in wb.sheetnames:
        wb[_zh].title = f'{_zh} {_vi}'
TAB_COUNTS = {(f'{k} {TAB_VI[k]}' if k in TAB_VI else k): v for k, v in TAB_COUNTS.items()}

for _t536 in wb.sheetnames:
    _w536 = wb[_t536]
    _w536.sheet_format.defaultRowHeight = 24
    for _r536 in range(1, _w536.max_row + 1):
        _w536.row_dimensions[_r536].height = 24

OUT = f'{GROUP}進度完整分析_{MMDD}.xlsx'
wb.save(OUT)
print('SAVED', OUT, '| tabs:', {k: v for k, v in TAB_COUNTS.items()})

M = lc.RunManifest(input_xlsx=INPUT)
M.set_versions({'snapshot': {'version': PRE['snapshot_version']}, 'dictionary': {'version': DICT_VER},
                'closure_whitelist': {'version': 3, 'active_entries': PRE['whitelist_active_entries']},
                'sheet4_whitelist': f"字典內建(R-v537-1·{len(WL4['entries'])}筆·棘輪≥{WL4.get('ratchet_min')})",
                'answer_rejected_R_v539': N_ARJ, 'ntns': f'v{NTNS_VER}',
                'interval_89_files': PRE['interval_89_files'], 'sheet4_enabled': SHEET4_GATE,
                'sheet4_gate_R_v527_1': COV,
                'inventory': (f'{INV_NAME}({INV_NROWS}列·疑截斷)' if INV_TRUNC else INV_NAME),
                'brand_overrides': 'v1.1', 'group': GROUP})
M.set_tab_counts(TAB_COUNTS)
mp = M.finalize('pending-regressions')
print('manifest:', mp)

import json as _json3
_json3.dump({'run_date': str(datetime.date.today()), 'input_file': OUT, 'tab_row_counts': TAB_COUNTS},
            open('/mnt/user-data/outputs/dpr_tab_counts_latest.json', 'w', encoding='utf-8'),
            ensure_ascii=False, indent=1)
print('sidecar: /mnt/user-data/outputs/dpr_tab_counts_latest.json 已落地（R-v505-1）')
