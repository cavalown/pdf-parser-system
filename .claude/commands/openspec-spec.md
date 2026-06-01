---
description: 為 openspec change 的各 capability 撰寫 spec。用法：/openspec-spec <slug>
---

你是 pdf-parser-system 的 spec-driven 開發 AI。

使用者要求為 change `$ARGUMENTS` 撰寫 capability specs。

## 步驟

1. 讀取 `openspec/config.yaml`，了解專案規範。
2. 讀取 `openspec/changes/$ARGUMENTS/proposal.md`，取得 capabilities 清單。
3. 讀取 `openspec/specs/` 下既有的 spec.md 範例，了解格式。
4. 針對 proposal 中每個 **New Capability** 與 **Modified Capability**，撰寫 spec。
   - spec 格式：
     ```markdown
     ## Requirements

     ### Requirement: <requirement 名稱>

     <元件/系統> SHALL <具體行為描述>。

     #### Scenario: <情境名稱>

     - **GIVEN** <前提條件>
     - **WHEN** <觸發動作>
     - **THEN** <預期結果>
     - **AND** <額外結果（若有）>
     ```
   - 每個 requirement 至少要有一個可驗證的 scenario。
   - 跨 frontend/backend 行為放在 shared capability。
   - Frontend-only 行為獨立成 frontend capability。
   - Backend-only 行為獨立成 backend capability。
5. 將每個 spec 寫入：
   - 新 capability：`openspec/specs/<capability-slug>/spec.md`
   - 同時在 change 下也建立：`openspec/changes/$ARGUMENTS/specs/<capability-slug>/spec.md`
6. 向使用者條列寫完的 specs，並提示下一步可執行 `/openspec-design $ARGUMENTS`。

## 規範

- 使用正體中文撰寫，專有名詞與技術名詞維持英文。
- SHALL 語句要具體、可驗證，避免模糊描述。
- Scenario 的 GIVEN/WHEN/THEN 要對應真實的系統行為，不要寫成測試步驟。
