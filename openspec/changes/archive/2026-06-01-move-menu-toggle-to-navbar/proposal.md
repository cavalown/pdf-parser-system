## Why

目前 menu icon 位於 sidebar 區域，與 `PDF Fac.` brand 分離，導致全域導覽控制的位置不夠直覺。將 menu icon 移到 navbar 並放在 `PDF Fac.` 左邊，可以讓品牌與全域 sidebar 控制集中在同一個 top navigation 區域。

## What Changes

- 將 sidebar menu icon 從 sidebar 內移到 top navbar。
- Menu icon SHALL 位於 `PDF Fac.` 左邊。
- Navbar SHALL 使用暗紅色作為背景色。
- Menu icon 仍 SHALL 控制 sidebar expanded/collapsed state。
- `PDF Fac.` SHALL 繼續作為 home link，點擊導向 `/`。
- Sidebar SHALL 繼續只顯示 `PDF Analyze`、`PDF Modify`、`Setting` 三個分類。
- 保留既有首頁 `/api/health` service status 行為。

## Capabilities

### New Capabilities

- `navbar-menu-toggle`: 定義 top navbar 中 menu icon 與 `PDF Fac.` brand 的排列，以及 menu icon 對 sidebar 收合狀態的控制行為。

### Modified Capabilities

- 無。

## Impact

- 影響範圍：frontend。
- 主要影響檔案：
  - `frontend/src/App.tsx`
  - `frontend/src/App.css`
- 不影響 backend。
- 不影響 `/api/health` API contract。
- 不新增 npm dependencies。
