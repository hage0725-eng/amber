# DPR v3.5 → 過1.9口徑修正稿（R-1008-1／Q-1008-1）

對象：claude.ai Project 內 DPR v3.5（規格快照＋`dpr_suite.py` 內的 `build_dpr.py`）。
依據：`dpr_v35/` 冷備鏡像（規格 v572、builder v587）。Project 現行版較新（suite v652），套用前先在 Project 確認下列原文仍在。

## 結論
只有 `build_dpr.py` 一處要改：過1.9 現在要「取整後 > 0」才算逾期，改成「原值 > 0」。
過標準交期（col36）、過客戶交期（col38）本來就是原值 > 0，不動。

## 1. build_dpr.py（完整 diff 見 `build_dpr_R-1008-1.patch`）
在 `ERP_DEGENERATE_MIN = 365` 下一行加：
```python
R1008_1_FROM = datetime.date(2026, 10, 8)   # R-1008-1 生效日：過1.9 由取整>0 改原值>0
```
主分析迴圈裡：
```python
# 改前
    if _st37 == 'over' and o19 > 0:
# 改後
    # R-1008-1（Amber 2026-10-08）：過1.9 改原值>0（0.38 天也算，顯示「0天」）；10/7 以前沿用取整舊口徑
    if _st37 == 'over' and (TODAY >= R1008_1_FROM or o19 > 0):
```
- `erp_days()` 三態編碼（R-v551-2，>365 退化序號＝無基準）完全不動，A8 棒不受影響。
- OTD 引擎 `otd_of()` 只看狀態（準時／逾期），不受影響。
- 原因文字仍用 `math.floor(o19)`，0.38 天顯示「過1.9交期0天」。

## 2. 規格快照「四、主分析異常引擎」第二點改成
> - 過 1.9 交期（col37 原值 > 0；**R-1008-1 自 2026-10-08 起不取整，0.38 天也算**；10/7 以前報告沿用取整重現）二次判定：生管 Mail(col7) 無→delay；Mail 已逾→delay；Mail 未逾→not_delay 警告。

## 驗證（本 repo 已做）
`specs/verify/verify_1p9.py` 用 0818／0916 黃金樣本 11,412 個過1.9 值，比對 builder 與規則庫引擎：

| 分析日 | 現行 builder 不一致 | 修正後不一致 |
|---|---|---|
| 10/7 | 0 | 0（舊口徑照舊） |
| 10/8 起 | 105（0～1 天之間的值） | 0 |

重跑：`python specs/verify/verify_1p9.py .`（在 paiho-workflow 資料夾執行）

## 套進 Project 後
1. 在 Project 跑 `dpr_suite.py gate`，全綠才算數。
2. 預期影響（0916 試算）：10 筆改變，7 筆 POTENTIAL→WARNING、3 筆 WARNING→DELAY。
3. 回報 Claude → Q-1008-1 改「已落地」，下一次 `/daily` 的 check_report 一致率應為 100%。
