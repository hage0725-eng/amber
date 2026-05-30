# dedup-final-structure.md — 2026-05-30
> 單一來源對照表。維護時以此為準，勿重複貼規則。

## 結構總覽

| 層級 | 路徑 | 載入模式 | 用途 | 單一來源 |
|---|---|---|---|---|
| User config | /root/.claude/settings.json | config | Stop hook + Skill 權限 | ✅ 此處唯一 |
| User hook | /root/.claude/stop-hook-git-check.sh | hook（Stop） | 強制 commit/push 後才允許停止 | ✅ 此處唯一 |
| User skill | /root/.claude/skills/session-start-hook/SKILL.md | skill（按需） | 建立 SessionStart hook 的工作流程 | ✅ 此處唯一 |
| Project | /home/user/amber | — | 目前無任何 Claude 設定，可按需新增 | — |

## 維護規則
<!-- 維護備註：去重後單一來源，勿重複貼規則 -->
- git-safety 邏輯唯一來源：`stop-hook-git-check.sh`，勿在 CLAUDE.md 重述
- session-start-hook 步驟唯一來源：`SKILL.md`，勿在 CLAUDE.md 重述
- 每月用 `/memory` 指令檢查載入清單是否有新重複或衝突

## PHASE 5 驗證結果

| 項目 | 改前 | 改後 | 結果 |
|---|---|---|---|
| 啟動全載 token | 0 | 0 | ✅ 不變 |
| skill 按需 context（呼叫時） | ~154 行 | ~66 行 | ✅ 省 88 行（-57%） |
| Stop hook 行為 | exit 2 on uncommitted/unpushed | 同上 | ✅ 不變 |
| Skill 步驟完整性 | 8 步驟 | 5 步驟（合併驗證為一節） | ✅ 行為等價，無遺漏 |

## 總結
- **context 變化**：啟動全載 0→0（無變化）；skill 按需呼叫時省 88 行
- **harness 行為**：完全等價，Stop hook 邏輯、skill 工作流程步驟均保留
- **無需回退**任何 change-set
