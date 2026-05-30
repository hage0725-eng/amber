# dedup-decision-sheet.md — 2026-05-30
> PHASE 2 產出。GATE 1：請逐列批准後才進入 PHASE 4。

## 正規化說明
所有 15 條原子規則分屬三個載入模式（config / hook / skill），無跨 scope 重複，無語意衝突。
交叉矩陣只有 USER_SCOPE 單欄，PROJECT_1 全空，無 DUPLICATE / CONFLICT 可處理。

---

## 決策表

| # | 涉及 rule_id | 類別 | 建議動作 | 目標位置 | 依據 | 行為影響 | 預估省下(行) |
|---|---|---|---|---|---|---|---|
| 1 | USER-settings-01, USER-settings-02 | — | keep-canonical | settings.json（現狀） | 設定精簡（19行），無冗餘 | none | 0 |
| 2 | USER-hook-01~07 | — | keep-canonical | stop-hook-git-check.sh（現狀） | Hook 邏輯完整、必要；屬強制行為，不可改為建議 | none | 0 |
| 3 | USER-skill-01~06 | ALWAYS-ON→ON-DEMAND | keep-canonical（已是 skill） | skills/session-start-hook/SKILL.md（現狀） | 已正確設為按需載入，非 launch-full，無需移動 | none | 0 |
| 4 | USER-skill-01~06 | — | rewrite-shorter（可選） | SKILL.md | 154 行，按需載入時仍佔 context；可精簡說明性文字、保留核心步驟，目標 ~80 行 | low（僅影響 skill 引導文字，不影響 harness 行為） | ~74 |
| 5 | PROJECT_1 全體 | — | 無動作 | — | 專案完全空白，無任何規則需處理 | none | 0 |

---

## REVIEW 項目
- **無**：所有項目行為影響皆為 none 或 low（#4 為可選）。

## 彙整
- **CONFLICT**：0 件
- **DUPLICATE**：0 件
- **MISPLACED**：0 件
- **STALE**：0 件
- **ALWAYS-ON→ON-DEMAND**：0 件需處理（skill 已正確按需）
- **可選優化**：1 件（#4，SKILL.md rewrite-shorter，~74 行）

---

## 給您的選擇

**#4（SKILL.md 精簡）** 是唯一可做的動作：
- 現況：154 行，每次呼叫此 skill 都會載入全部內容
- 建議：精簡到 ~80 行，只保留必要步驟與程式碼片段，移除冗長說明文
- 行為影響：low — Claude 引導 session-start-hook 的步驟不變，只是措辭更緊湊
- 若不做：完全沒問題，現狀已很乾淨

若您批准 #4，進入 PHASE 4 時我會對 SKILL.md 做 rewrite-shorter；
若不批准（保持現狀），可直接跳到 PHASE 5 驗證，結論將是「無需變更，結構已最優」。
