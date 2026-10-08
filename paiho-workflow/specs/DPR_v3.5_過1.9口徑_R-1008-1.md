# DPR v3.5 → 過1.9口徑同步稿（R-1008-1／Q-1008-1）

給：claude.ai Project 內 daily-progress-review v3.5 規格。貼上後回報 Claude，再把 Q-1008-1 標「已落地」。

## 要改什麼
過1.9交期天數「是否逾期」從**取整後 > 0** 改成**原值 > 0**（內部從嚴，與過標準交期／過客戶交期一致）。
- 0.38 天也算逾期，顯示「0天」。
- 分析日 ≤ 2026-10-07 的報告沿用取整舊口徑，才能重現 0818／0916 黃金樣本。
- 依據：`core/rules.yaml` → `dpr.positive_test.over_1p9: raw`、`dpr.positive_test_history`。

## 1. 天數欄取整（0B）
`過1.9交期天數` 從「一律 floor」清單**移出**；判定用原值，顯示時才取整。

```python
DAY_COLS = [c for c in DAY_COLS if not c.startswith('過1.9交期天數')]   # 判定要用原值
```

## 2. 過1.9 判定（取代 0D 的 calc_1p9 開頭）
```python
OLD_1P9_UNTIL = dt.date(2026, 10, 7)          # R-1008-1 前用取整
excel_epoch = datetime(1899, 12, 30)

def over_1p9_days(v):
    """回傳逾期天數（float），未逾期回 NaN。"""
    v = pd.to_numeric(v, errors='coerce')
    if pd.isna(v): return np.nan
    if v > 365:                                # 被存成 Excel 日期序號 → 反推
        diff = (today.date() - (excel_epoch + timedelta(days=int(v))).date()).days
        return float(diff) if diff > 0 else np.nan
    if today.date() <= OLD_1P9_UNTIL:          # 舊口徑
        return float(np.floor(v)) if np.floor(v) > 0 else np.nan
    return float(v) if v > 0 else np.nan       # R-1008-1：原值 > 0

active['over_1p9'] = active['過1.9交期天數\nQua ngày giao 1.9'].apply(over_1p9_days)

def calc_1p9(row):
    v = row['over_1p9']
    if pd.isna(v): return ('none', '')
    n = int(np.floor(v))                       # 顯示用；0.38 天顯示「0天」
    ...（以下 H欄 Mail 二次判定不變，訊息中的 int(v) 改用 n）
```

## 3. anomaly_logic.md 修正A 補一行
> 例外：過1.9交期天數判定用原值 > 0（R-1008-1，2026-10-08 起）；顯示仍取整。

## 預期影響
0916 試算 10 筆改變：7 筆 POTENTIAL→WARNING、3 筆 WARNING→DELAY。
貼上後下一次 `/daily`，`check_report` 一致率應回到 100%。
