# Paiho T組工作流（paiho-workflow）

Amber Lin（越南百和 北區業務經理）的規則庫與自動化。對話用中文；
回報格式：第一句寫結論；一點一段，多點用 1. 2. 3.，結果用 ==> 標示。
用團隊用語（TDT、HC、NK、CS、預告、胚帶、催、審、對色），公司名一律寫「百和」。

## 鐵則
1. **規則只寫在 `core/rules.yaml`**，程式與 skill 不得寫死門檻。
2. 改了 `core/ dpr/ tools/ tests/` 任何檔案 → 必跑 `python tools/gate.py`，全綠才可 commit。
   （hook 會自動跑；pre-commit 也會擋）
3. 新裁示先登錄 `core/decisions.csv`（id, date, by, content, affects, status），
   再改 rules.yaml，status 改「已落地」。
4. 不得臆測欄位或代碼意義 → 標「待確認」並問 Amber。
5. 不得修改 `tests/golden/` 的期望值來讓測試變綠；黃金樣本只能由
   `tools/make_golden.py` 從 Amber 已確認的分析檔產生。
6. 產出檔：不凍結窗格、顯示格線、表格黑框線、日期 M/D。
7. 越南現場：異常一律框定為流程缺口，不指向個人；副總層只用客戶簡稱。
8. 回填合併只寫「回填欄」；驗證失敗程式會中止，不得手動補救後交出。
9. 給組員的越文說明一律正式語氣。

## 檔案地圖
| 路徑 | 用途 |
|---|---|
| core/rules.yaml | 共用規則（DPR 門檻、89、KN/LL/XLBT、站別、材料排除、備料%、客戶群） |
| core/decisions.csv | 裁示登錄表 |
| core/paiho_core.py | 規則載入、日期/數值解析、站別 |
| dpr/engine.py | daily-progress-review 異常等級／風險判定核心 |
| tools/gate.py | 回歸守門（G1–G7） |
| tools/check_report.py | 用規則庫重判任一份分析檔，抓 skill 漂移 |
| tools/make_golden.py | 由已確認分析檔產生黃金樣本 |
| flow/intake.py | 閘門 A：班長 ERP 原檔健檢（停線才找 Amber） |
| flow/backfill.py | 回填拆檔（每助理一份）／收回合併（只寫回填欄、逐格驗證） |
| flow/digest.py | 給 Amber 的每日摘要 |
| tests/approved.yaml | Amber 核定門檻（凍結；G6 邊界案例以此為準，改動須經 /ruling＋Amber 確認） |

## 指令
- `/daily <檔案>`：每日進度彙整＋規則庫第二意見
- `/ruling <裁示內容>`：登錄裁示並落地到 rules.yaml
- `/gate`：跑回歸守門
- `/intake <原檔> <狀態夾>`：閘門 A
- `/split <分析檔> <輸出夾>`：回填拆檔
- `/collect <分析檔> <交回夾> <輸出夾>`：收回合併＋摘要
