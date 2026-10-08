---
description: 每日 T組進度彙整，並用 paiho-core 規則庫做第二意見
argument-hint: <T組進度追蹤表路徑> [分析日 YYYY-MM-DD，預設今天]
---
對 $ARGUMENTS 執行每日進度彙整：

1. 用 daily-progress-review skill 產出 Excel＋Word（照 skill 規格）。
2. 產出後跑：`python tools/check_report.py <產出的分析檔> <分析日>`
3. 回報（照 CLAUDE.md 格式）：
   - 第一句：今天 DELAY / WARNING / POTENTIAL 筆數與最大風險客戶
   - 規則庫一致率；若不是 100%，列出差異筆數並判斷是 skill 漂移還是規則庫需更新，
     需要 Amber 決定的列在最後並以問句結尾
   - `python tools/gate.py` 的 G7 若有「待裁示」，附在最後提醒
