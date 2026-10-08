---
description: 登錄 Amber 的新裁示，並落地到共用規則庫
argument-hint: <裁示內容>
---
新裁示：$ARGUMENTS

1. 讀 core/decisions.csv，給新 id（格式 R-MMDD-n，今天日期），新增一列 status=已裁示。
2. 判斷影響哪支 skill、要改 rules.yaml 哪個鍵；只能改 rules.yaml，不得把門檻寫進程式。
   若規則需要新判斷邏輯，改 dpr/engine.py 並在 tools/gate.py 的 boundary_cases 加一個邊界案例。
3. 跑 `python tools/gate.py`：
   - 全綠 → status 改「已落地」，note 寫改了哪個鍵
   - 紅燈且是因為裁示「本來就會改變」歷史判定 → 停下來，列出受影響筆數給 Amber 確認，
     不得自行改黃金樣本
4. 回報改了什麼、gate 結果，需要 Amber 決定的事以問句結尾。
