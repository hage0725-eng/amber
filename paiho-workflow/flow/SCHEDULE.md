# 影子期排程定義（尚未建立，等 Amber 開 01_原檔_inbox 權限後一次建好）

通知：手機推播（push），不寄 Email；每次執行自成一個對話窗，Amber 可直接在裡面追問（R-1008-3）。
組員端：影子期不發送任何檔案或訊息（R-1008-4）。
時區：Asia/Ho_Chi_Minh；週一至週六。

Drive 資料夾（CLAUDE / DPR_自動化（影子期））
| 資料夾 | ID |
|---|---|
| 根 | 13qQiEvphndZnuOk1XUfjU5dY19bNIh_y |
| 00_程式 | 1EBBLOeLjmvdlShhgeKDUBJl8WKJlqsWe |
| 01_原檔_inbox | 1bOOjXepSxp5CytwQchowrnVIrdFtvyuQ |
| 02_分析輸出 | 16fAWtvzVLuiut6pZ5JlG_h5gAjuzKuoe |
| 03_回填分派_影子 | 1v8gwedF5vvXxaH3Me7JlspiIrK9VfDkF |
| 04_回填交回_影子 | 16VSsIjKZtX9t5z-oRqAfeVFsIrzGdFBk |
| 05_回填彙總與摘要 | 1znYHBvVckhsQreZ_DHYlbUJZDK81PUB2 |
| 06_狀態紀錄 | 1ErmmABlpshwWQrBy33NWC6RFOvgNHQgs |

## 任務 1｜閘門 A（每日 9:47）
1. 從 00_程式 下載最新 paiho-workflow zip，解壓，安裝 requirements.txt
2. 從 06_狀態紀錄 下載 intake_history.csv（沒有就首次執行）
3. 在 01_原檔_inbox 找今天修改的最新檔；沒有 → 推播「班長尚未放原檔」並結束
4. 執行 `python flow/intake.py <檔> state --mtime <Drive modifiedTime>`
5. 把 intake_history.csv 傳回 06_狀態紀錄
6. 推播第一句結論；停線時列原因、哪位班長、ERP 匯出步驟

## 任務 2｜回填拆檔（每日 11:47，DPR 尚未產出則 14:47 再試一次）
1. 在 02_分析輸出 找今天的「T組進度完整分析_MMDD.xlsx」；沒有 → 推播「今天 DPR 尚未產出」並結束
2. `python flow/backfill.py split <分析檔> out`
3. 上傳到 03_回填分派_影子/MMDD/（只有 Amber 看得到）
4. 推播：幾份、每人幾列、未指派幾列

## 任務 3｜收回與摘要（每日 16:47）
1. 下載當天分析檔與 04_回填交回_影子 內所有檔
2. `python flow/backfill.py collect <分析檔> back res`
3. `python flow/digest.py state res/<檔名>_回填狀態.xlsx`
4. 彙總檔、狀態表上傳 05_回填彙總與摘要；摘要全文推播
5. 合併驗證失敗 → 不上傳彙總檔，推播「驗證失敗＋原因」
