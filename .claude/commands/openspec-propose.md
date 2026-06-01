---
description: 為 openspec change 起草 proposal。用法：/openspec-propose <slug>
---

你是 pdf-parser-system 的 spec-driven 開發 AI。

使用者要求為 change `$ARGUMENTS` 起草一份 proposal。

## 步驟

1. 讀取 `openspec/config.yaml`，了解專案規範。
2. 讀取 `openspec/changes/` 下既有的 proposal.md 範例，了解格式。
3. 詢問使用者：「這個 change 要解決什麼問題？要改什麼？」，等待使用者描述需求。
4. 根據使用者描述，起草 proposal，格式包含：
   - **Why**：為什麼需要這個 change（現況問題、動機）
   - **What Changes**：具體的改動內容
   - **Capabilities**：新增或修改的 capabilities 清單（New Capabilities / Modified Capabilities）
   - **Impact**：影響範圍（Frontend / Backend / Shared / API contract）
5. 將 proposal 寫入 `openspec/changes/$ARGUMENTS/proposal.md`。
6. 建立 `openspec/changes/$ARGUMENTS/.openspec.yaml`，格式：
   ```yaml
   schema: spec-driven
   created: <今天日期 YYYY-MM-DD>
   ```
7. 將 proposal 內容向使用者摘要說明，並提示下一步可執行 `/openspec-spec $ARGUMENTS`。

## 規範

- 使用正體中文撰寫，專有名詞與技術名詞維持英文。
- 清楚標示影響範圍是 shared、frontend、backend，或跨多端。
- 若需求會影響 API contract，必須在 Impact 中明確列出。
