## Why

目前 frontend 的 app shell、sidebar navigation、首頁 health check 與 placeholder 工作區都集中在單一 `App.tsx`，sidebar 項目也只是同頁錨點。隨著 `PDF Analyze`、`PDF Modify`、`Setting` 需要成為各自獨立頁面，frontend 需要先建立清楚的 route 與 page component 邊界，避免後續功能持續塞進首頁 component。

## What Changes

- 將 frontend 從單一錨點式 dashboard 調整為 route-based page shell。
- 將首頁拆成獨立 `HomePage`，目前只負責顯示 backend 連線狀態與重新檢查操作。
- 將 sidebar navigation 項目對應到獨立頁面：
  - `/`：首頁連線狀態
  - `/analyze`：`PDF Analyze`
  - `/modify`：`PDF Modify`
  - `/settings`：`Setting`
- 保留 top navbar、`PDF Fac.` home link、sidebar expanded/collapsed、collapsed hover/focus label，以及紅黑 design system。
- 新增 route-aware active navigation 行為，讓 sidebar active item 反映目前頁面。
- `PDF Analyze`、`PDF Modify`、`Setting` 先建立頁面 component 與基本空狀態，不實作 PDF 分析、修改或設定表單功能。

## Capabilities

### New Capabilities

- `frontend-routed-pages`: 定義 frontend route-based page shell、首頁 health status page，以及 sidebar 項目對應獨立頁面的行為。

### Modified Capabilities

- `frontend-navigation-shell`: 將 sidebar navigation 從同頁錨點改為 route navigation，並要求 active item 依照目前 route 顯示。
- `frontend-dashboard-shell`: 將首頁 dashboard scope 收斂為獨立首頁 health status page，不再承載 sidebar 其他分類的 placeholder 區塊。

## Impact

- Frontend：影響 `frontend/src/App.tsx`、frontend component/page 結構、navigation link 行為與 styles。
- Dependencies：可能新增 `react-router-dom` 作為 route navigation dependency。
- Backend：不影響 backend API，`GET /api/health` contract 不變。
- Shared/API contract：不變，frontend 仍透過 `/api/health` 檢查 backend 連線狀態。
