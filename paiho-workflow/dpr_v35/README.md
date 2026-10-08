# DPR v3.5 套件（自 Drive 冷備還原，2026-10-08）

來源：Drive「Paiho_Project歸檔／13_PACK重複檔與字典冷備」「14_DPR_套件歸檔」「12_制度檔」「04_夜間覆盤」。
全部檔案已逐一驗證：位元組數＝Drive fileSize、xz 拼接後 SHA-256 前 16 碼＝README 登錄值、xz CRC64 通過、
JSON 可解析、所有 .py 通過語法檢查（未執行任何下載的程式）。明細見 `_verify/MANIFEST.csv`（42 列 0 失敗）。

| 資料夾 | 內容 | 版本 |
|---|---|---|
| spec/ | SKILL_v3_5_完整規格_權威自足版_v572.md（1,435 行，SHA 與登錄簿一致）、v503 增補、0706 排查手冊、邊界補遺、冷備 README、hash 登錄簿(0914) | v572 |
| builder/ | build_dpr.py、ntns_db_fill.py、xlrd_shim.py（原名 xlrd.py，改名避免蓋掉真 xlrd） | build v587 |
| data/ | 回填原因處置字典_v85_columnar.json、ntns_dict_v505.json（NT 1,826／NS 684）、brand_code_overrides（內容 v1.5） | 字典 v85 |
| rollback/ | dpr_rollback v652→v632、v624→v621、rebuild_v620、版本沿革 | ⚠️ 缺 v625–v631 |

## ⚠️ 還不能獨立跑 DPR——缺主程式
1. **dpr_suite.py（現行 v652）**：只存在 Project。內含 `_PACK`（`restore` 可自癒還原 10 檔）、gate 回歸棒、classifier。
   所有 rollback 腳本都以它為輸入。
2. build_dpr.py 需要但這裡沒有：`dict_v14_codec.py`（讀 v85 columnar 字典）、`dpr_regression_live_common.py`、
   `sheet6_6b_結案白名單_v3.json`、各 `dpr_regression_v*.py`（推測都在 dpr_suite `_PACK` 內，拿到 suite 後 `restore` 即可）。
3. 每日資料（使用者檔，非程式）：T組追蹤進度表、`T組客戶清冊.XLS`／`T1組客戶清冊.XLS`（0914 已知 builder 硬相依）、
   品牌代碼對照表、庫存 DB、89DB 累積檔。
4. 路徑：builder 預設讀 `/home/claude/dpr`、`/mnt/project`、工作目錄；brand overrides 只讀工作目錄。
   之後接自動排程時由啟動腳本把 data/、builder/ 放到這些路徑，不改 builder 本身。
5. 版本落差：登錄簿為 0914（suite v594／字典 v74／NT/NS v499／builder v578），本套件為較新冷備；
   以 Project 現行 v652 為準，拿到 suite 後重新蓋章登錄簿。
