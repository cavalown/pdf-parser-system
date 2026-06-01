## Context

目前 frontend 已有 React + Vite app shell、紅黑色系、可收合 sidebar，以及首頁 `/api/health` 狀態區塊。但導覽 shell 的資訊架構與產品命名需要修正：

- 產品名稱應為 `PDF Fac.`，目前 UI 仍使用 `PDF Parser System`。
- 系統名稱應出現在 top navbar 左上方，目前在 sidebar 底部。
- menu icon 應在系統名稱區域下方並靠 sidebar 右側，目前在 sidebar 最上方左側。
- sidebar 分類應為 `PDF Analyze`、`PDF Modify`、`Setting`，目前仍是首頁/服務狀態/文件。

本變更只處理 frontend navigation shell，不改 backend 與 health API contract。

## Goals / Non-Goals

**Goals:**

- 建立 top navbar，讓 `PDF Fac.` 成為第一視覺入口與首頁 link。
- 調整 sidebar 結構，使 menu icon 位於 navbar 下方的 sidebar 區域，並靠右對齊。
- 將 sidebar navigation item 改為 `PDF Analyze`、`PDF Modify`、`Setting`。
- 保留 sidebar expanded/collapsed 狀態與 collapsed hover/focus label。
- 保留目前首頁 health check 行為與紅黑 design system。

**Non-Goals:**

- 不新增 PDF Analyze、PDF Modify、Setting 的實際頁面功能。
- 不導入 router 或多頁 routing。
- 不修改 backend API。
- 不新增 dependencies。
- 不重建整套 design system。

## Decisions

### Decision: 使用單一 App shell 結構承載 navbar、sidebar 與 main content

採用現有 `App.tsx` 的單一 app shell 方式，將 layout 明確切成：

```txt
app-shell
├── top-navbar
│   └── PDF Fac. home link
├── sidebar
│   ├── menu toggle
│   └── nav items
└── main-content
    └── existing home health status
```

理由：
- 目前專案尚未引入 routing 或多頁 layout abstraction，維持單一 shell 可降低變更範圍。
- 這次是 UI 結構修正，不需要新增全域 layout framework。

替代方案：
- 建立獨立 `Navbar`、`Sidebar` components。這會更利於擴充，但目前 app 規模仍小，立即拆分可能增加不必要檔案與抽象。

### Decision: 不新增 MUI dependency

雖然專案規範提到 UI library 使用 MUI，但目前 `frontend/package.json` 尚未安裝 MUI，既有 UI 也以 CSS 實作。這次變更 SHALL 沿用現有 CSS pattern，不新增 MUI dependency。

理由：
- 新增 MUI 會牽涉 dependency、theme provider 與 component migration，超出本次修正範圍。
- 本次需求可用現有 React + CSS 完成，且不影響後續導入 MUI。

替代方案：
- 安裝 MUI 並改用 `AppBar`、`Drawer`、`List`。這符合長期規範，但對目前小範圍修正成本較高，且會擴大驗證範圍。

### Decision: Sidebar items 先作為單層 navigation categories

`PDF Analyze`、`PDF Modify`、`Setting` 先作為單層 nav item 呈現，不新增子項目。

理由：
- 使用者只指定目前分類名稱，尚未定義子功能。
- 單層 nav 可保留 collapsed tooltip 行為，也方便未來擴充成群組。

替代方案：
- 直接設計為可展開分類群組。這需要定義子項目與 expanded state，需求尚未明確。

### Decision: Collapsed state 保留 icon 與 hover/focus label

沿用目前 collapsed sidebar 的互動意圖：展開時顯示文字，收合時只顯示 icon，hover/focus 顯示 label。

理由：
- 這是既有需求的一部分，且符合狹窄 sidebar 的可用性。
- keyboard focus label 可維持基本可及性。

替代方案：
- 收合後完全隱藏 sidebar。這會降低常用 navigation 的可見性，不符合「只剩 icon 時要能 hover」的原始要求。

## Risks / Trade-offs

- [Risk] Top navbar 與 sidebar 同時存在，可能在 mobile viewport 產生擁擠。 → Mitigation：使用 responsive CSS，讓 navbar 固定在上方，sidebar 在窄螢幕可水平或緊湊排列，避免文字溢出。
- [Risk] 使用字母 icon 代表三個分類辨識度有限。 → Mitigation：短期可用穩定文字縮寫，後續若導入 icon library 或 MUI icons，再替換成語意 icon。
- [Risk] 未導入 MUI 可能與專案長期規範不一致。 → Mitigation：本次不新增 dependency，並將 CSS tokens 保持清楚；未來導入 MUI theme 時可映射現有 red/black tokens。
- [Risk] 目前沒有 frontend component tests。 → Mitigation：本次至少執行 `npm run lint` 與 `npm run build`，必要時用瀏覽器人工檢查 expanded/collapsed 與 hover/focus 行為。
