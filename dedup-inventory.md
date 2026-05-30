# dedup-inventory.md — 2026-05-30

## 範圍設定
| Scope | 路徑 |
|---|---|
| USER_SCOPE | /root/.claude |
| PROJECT_1 | /home/user/amber |
| MANAGED | 無（/etc/claude-code/ 不存在） |

---

## 檔案盤點

| path | 行數 | 載入模式 | 一句用途 |
|---|---|---|---|
| /root/.claude/settings.json | 19 | config | 全域設定：Stop hook 與 Skill 權限 |
| /root/.claude/stop-hook-git-check.sh | 58 | hook | Stop hook：確認 git commit/push 才允許停止 |
| /root/.claude/skills/session-start-hook/SKILL.md | 154 | skill（按需） | 建立 SessionStart hook 的完整工作流程 |
| PROJECT_1 任何 Claude 設定檔 | — | — | 不存在，PROJECT_1 無任何指令來源 |

---

## 原子規則清單

| rule_id | 載入模式 | 主題標籤 | 規則一句話 | 來源 path:行 |
|---|---|---|---|---|
| USER-settings-01 | config | permission | 允許呼叫 Skill 工具 | settings.json:17 |
| USER-settings-02 | hook | git-safety | Stop 時執行 stop-hook-git-check.sh | settings.json:4-14 |
| USER-hook-01 | hook | recursion-guard | stop_hook_active=true 時直接 exit 0 防止遞迴 | stop-hook-git-check.sh:7-10 |
| USER-hook-02 | hook | git-safety | 非 git repo 時 exit 0 跳過 | stop-hook-git-check.sh:13-15 |
| USER-hook-03 | hook | git-safety | 無 remote 時 exit 0 跳過 | stop-hook-git-check.sh:18-24 |
| USER-hook-04 | hook | git-safety | 有未提交變更時 exit 2 並提示 commit | stop-hook-git-check.sh:27-30 |
| USER-hook-05 | hook | git-safety | 有 untracked 檔案時 exit 2 並提示 commit | stop-hook-git-check.sh:33-37 |
| USER-hook-06 | hook | git-safety | 有未推送 commits（remote branch 存在）時 exit 2 | stop-hook-git-check.sh:41-46 |
| USER-hook-07 | hook | git-safety | 有未推送 commits（無 remote branch）時 exit 2 | stop-hook-git-check.sh:49-54 |
| USER-skill-01 | skill | session-setup | 分析專案依賴並建立 SessionStart hook 安裝腳本 | SKILL.md:59-65 |
| USER-skill-02 | skill | session-setup | hook 預設同步執行，用戶要求時才改 async | SKILL.md:75 |
| USER-skill-03 | skill | session-setup | hook 只為 web 環境（$CLAUDE_CODE_REMOTE）撰寫 | SKILL.md:76 |
| USER-skill-04 | skill | session-setup | hook 必須冪等且非互動式 | SKILL.md:79-80 |
| USER-skill-05 | skill | session-setup | 完成後驗證 hook 執行、linter、測試 | SKILL.md:119-134 |
| USER-skill-06 | skill | session-setup | 最後 commit 並 push 到遠端 branch | SKILL.md:137-138 |

---

## 各 scope 摘要

| Scope | 檔案數（會進 context） | 原子規則數 | 啟動全載行數 |
|---|---|---|---|
| USER_SCOPE | 3（config×1, hook×1, skill×1） | 15 | 0（skill 按需；hook 不注入 prose） |
| PROJECT_1 | 0 | 0 | 0 |
| **合計** | **3** | **15** | **0** |

---

## 各範圍可疑點摘要

**USER_SCOPE：**
1. Stop hook 強制性高（exit 2），在無 remote 情境下有豁免邏輯，但離線或 fork-only 可能仍受影響。
2. 無 CLAUDE.md — USER_SCOPE 無任何全域提示詞，無使用者層級自訂指令。
3. session-start-hook SKILL.md 154 行，按需載入時上下文量不小；若頻繁使用，可考慮精簡。
4. policy-limits.json 存在但不在本次盤點範圍內，建議另行審查。

**PROJECT_1 (amber)：**
1. 完全空白，無任何 Claude 設定，如有需要須從零建立。
