# SKILL v3.5 完整規格 — 權威版 v503 增補（Amber 2026-07-07 核可）

產生日：2026-07-07｜基準：v502 增補（本檔為自含快照提案；核可後取代 v502 成為唯一權威） 閘門狀態：0707 全綠 10/10（run\_manifest\_20260707-020230.json）

## 〇、本版新增裁決提案（待核可）

### R-v503-1 死預告家族「路由層覆蓋」

- 條件：orders 記錄 status=OPEN，但最新 raw\_reason 含「KHÔNG CÒN ĐƠN」家族語句（含 KH KHÔNG CÒN ĐƠN／…ĐƠN SD 等變體，正規化後子字串比對）。  
- 行為：路由層直接覆蓋為 ⛔FORCE → Sheet6 強制三選一（①XSD刪單②轉組③採購凍結），不進 6觀察、不得監控等待。  
- 依據：Amber 0701 裁決「死預告禁被動監控」；0613 舊回填批次（分類器上線前）遺留 OPEN 狀態為根因。0707 實測覆蓋 4 筆（226−222=4 由逾期回歸轉列 FORCE）。  
- 例外：status=PROCESSING（處理中）不覆蓋，維持字典後續裁決。  
- 迴歸：dpr\_regression\_v499\_backfill\_classify.py（重建版）斷言 Sheet6 上 KHÔNG CÒN ĐƠN SD 列生命週期必為 FORCE（處理中除外）。  
- 語義鐵律不變：CHƯA CÓ ĐƠN（尚未=活）→ OPEN 觀察；KHÔNG CÒN（已無=死）→ FORCE。

### R-v503-2 NT/NS 降級態（v477 檔案缺失事故處置）

- 觸發：預檢偵測 ntns\_dict\_v477.py/.json 缺失（本應保留勿刪，v502 檔案治理誤刪）。  
- 行為：退用 v475 之 23 個合規全碼鍵（len≥5，R-v496-1 精確比對不變，嚴禁前綴推導）；Sheet8 掛 banner「勿重工·待 v477 回傳」；Sheet8 本輪不派工；主分析 NT/NS 欄顯示 待人工判定/Chờ XN。  
- 解除：Amber 回傳 v477 檔後自動恢復 391 鍵，Sheet8 自動收斂。  
- 81H55002V、81TB527VM 維持 Amber 0629 留白待判，任何模式下不得推測。

### R-v503-3 迴歸鏈重建登錄（session 重建·10 棒）

專案內 dpr\_run\_all\_regressions.py / dpr\_regression\_live\_common.py 為 0701 舊版（6棒鏈引用已刪腳本）；v494/v497鎖定/v499回填分類 三支遺失；v495 為 0627 舊版與 v496 現制衝突。本輪依快照重建，新鏈如下（交付前必跑、全綠才交付）：

1. dpr\_regression\_v15\_roundtrip.py — 字典 v15 自身往返無損＋不變量（orders=1728·cap=111·phrase=45…）  
2. dpr\_regression\_v501\_whitelist\_prune.py — 白名單 v3 活性0＋存證146（v2 缺檔時以 audit\_index 為基準）  
3. dpr\_regression\_v494\_seq\_dedup.py（重建）— 4b/6/6b 欄位契約、去重唯一行鍵、6b≥2 不同單、Sheet4 兩態  
4. dpr\_regression\_v495\_layout\_borders\_v502.py（重建·兩態）— Sheet4 ①②並列或佔位、4b 必備欄、Sheet8 色號欄（banner 相容）、黑框線  
5. dpr\_regression\_v496\_ntns\_exact\_動態探針版.py — 精確比對、無前綴殘留、Sheet8=獨立真值  
6. dpr\_regression\_v497\_watchlist\_lock.py（重建）— cap🛑 列處置含🔒＋不得等後單、無等待詞、逾期欄≠監控中  
7. dpr\_regression\_v499\_backfill\_classify.py（重建）— CHƯA CÓ×cap 鎖定、非cap 含觀察、KHÔNG CÒN→FORCE  
8. dpr\_regression\_v500\_shared89\_v502.py（重建·兩態）— FIFO 分攤或 R-v502-2 佔位態  
9. dpr\_regression\_priority\_markers.py — ⭐/🆘 一律高風險、\_f\_major 定義一致  
10. dpr\_regression\_v502\_pipeline\_perf.py — E1-E4 效能與快取契約 主控：dpr\_run\_all\_regressions\_v502.py（計時＋紅燈存證＋run\_manifest）

## 一、有效規則登錄表（v503 全量）

R-v503-1 死預告家族路由覆蓋（新·提案）｜R-v503-2 NT/NS 降級態（新·提案）｜R-v503-3 迴歸鏈重建（新·提案） R-v502-1 管線效能 E1-E4（共享讀檔·parquet快取·分段計時·預檢）｜R-v502-2 89DB 佔位保護（\<12 檔→Sheet4/4s 佔位·非異常·不派工·自動解除） R-v501-1 結案白名單 v3 剪枝（活性0·audit\_index 存證146） R-v500-1 共用89 FIFO 分攤（先下單先佔·互斥·短缺屬實） R-v499-1 字典 columnar 編解碼（load\_any 透明讀取）｜6b 語句 CLOSED 覆蓋→Sheet9 R-v498-1 orders 圖=唯一真值（最新回填日勝）｜R-v498-2 CHƯA CÓ=活/KHÔNG CÒN=死 語義鐵律 R-v497-1 逾期回歸生命週期（逾期→重回填→cap）｜R-v497-2 cap🛑 鎖定禁三進·強制三選一·不得等後單｜R-v497-3 回填語句分類驅動狀態 R-v496-1 NT/NS 全碼精確比對（len≥5·嚴禁前綴推導）｜68QE756VA=NT（Amber 0629 特裁） R-v495-1 Sheet4 ①②逐列並列｜R-v495-2 4b 已掛89(DC)/保留量欄｜R-v495-3 Sheet8 色號欄｜R-v495-4 黑框線 FF000000｜R-v495-5 回填版面 R-v494-1 欄位契約單一事實來源｜R-v494-2 禁「建議」欄 R-v493-1 Sheet4 嚴格早於才算異常（同日=SOP豁免）｜R-v493-2 89DB 佔位守則｜R-v493-3 6b 欄位契約＋庫存誤開🟣 R-v492-1 cap 三選一（XSD/轉組/凍結）｜R-v487-1 4b BL=0｜R-v486-1 CLOSED/PROCESSED 前置排除 0704/0706 回填版面：異常檢查回報清空+黃底（待新輸入）｜處理進度=系統判定藍字｜舊回填紀錄(歷史)灰底尾欄 DGT FAIL=DELAY 無豁免（Amber 0622）｜⭐優先/🆘重大 無條件高風險｜col41=✔ 全表排除｜021280 BESTELLAR=0A6 BROOKS/江忠穎（永久）

## 二、輸出規格（§七·13+3 分頁）

0.說明｜1.主分析(54欄·隱藏89與OK列)｜2.統計｜3.樣品量產預告｜4.應掛未掛(兩態)｜4w.白名單｜4s.共用89餘量不足(兩態)｜4b.正式單×預告庫存｜6.預告未保留使用｜6觀察名單｜6b.重複開單群組｜7w.品牌空白｜8.NTNS未分類(降級態勿重工)｜9.已結案移除｜分類彙總｜派工清單 派工原則：強制（FORCE＋cap🛑）限期次日；常規（逾期回歸/新列/4b/6b未消化）限期+3日；限期一律為建議值非承諾；Sheet8 降級態不派工；VP 層只用客戶簡稱。

## 三、版本堆疊（0707 實測）

快照 v503提案(基準v502)｜字典 v15 columnar(orders=1728)｜NT/NS v475降級態23鍵(待v477回傳391鍵)｜Sheet4白名單 v2.7(80·雙鍵)｜結案白名單 v3(活性0/存證146)｜庫存 DB\_7\_1.xlsx(65,149列)｜品牌覆蓋 v1.1｜89區間檔 0/12(佔位態)

## 四、待 Amber 核可／行動

① R-v503-1/-2/-3 已核可（本檔為唯一權威·v501/v502 增補可刪） ② 回傳 ntns\_dict\_v477.py/.json（標記保留勿刪但實際缺失） ③ 回傳 12 支歷史 89 區間 XLS（6-8 位數字檔名）→ 自動解除 R-v502-2 佔位 ④ 81H55002V／81TB527VM 判定仍待裁決 ⑤ 本輪重建之 10 支迴歸＋live\_common＋總閘門請上傳回 PROJECT FILES（清單見 PROJECT\_FILES\_刪除與回傳清單\_v503.md）  
