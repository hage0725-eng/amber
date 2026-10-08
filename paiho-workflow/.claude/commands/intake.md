---
description: 閘門 A：檢查班長今天的 ERP 彙總原檔
argument-hint: <原檔> <狀態資料夾> [--mtime Drive修改時間] [--accept]
---
執行 `python flow/intake.py $ARGUMENTS`。停線時列出原因、哪位班長、哪一步（ERP 匯出），
筆數大幅變動要 Amber 確認屬實才可加 --accept 重跑，不得自行加。
