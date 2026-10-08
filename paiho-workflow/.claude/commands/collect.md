---
description: 收回組員回填檔，合併回分析檔原位並產出狀態表與摘要
argument-hint: <T組進度完整分析_MMDD.xlsx> <交回資料夾> <輸出資料夾>
---
1. 執行 `python flow/backfill.py collect $ARGUMENTS`
2. 執行 `python flow/digest.py <狀態資料夾> <輸出資料夾>/<檔名>_回填狀態.xlsx`
3. 把摘要原樣回給 Amber（已是她的格式）。合併驗證失敗時程式會中止且不留彙總檔——照實回報，不得手動修補後再交。
