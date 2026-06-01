## Why

目前首頁導覽 shell 與產品命名不符合需求：系統名稱仍使用 `PDF Parser System` 且放在 sidebar 底部，menu icon 的位置也不符合預期。這會讓後續 PDF 分析、修改與設定功能的資訊架構一開始就偏離產品方向，因此需要先修正 frontend navigation shell。

## What Changes

- 將系統名稱統一修正為 `PDF Fac.`。
- 建立 top navbar，並將 `PDF Fac.` 放在 navbar 左上方，點擊可回首頁。
- 調整 sidebar toggle menu icon：位置在系統名稱區域下方，並靠 sidebar 右側。
- 將 sidebar navigation 分類改為 `PDF Analyze`、`PDF Modify`、`Setting`。
- 保留 sidebar 收合能力；收合後仍只顯示 icon，並在 hover 或 keyboard focus 時顯示對應分類名稱。
- 保留既有紅黑基底 design system 與首頁 health check 行為。

## Capabilities

### New Capabilities

- `frontend-navigation-shell`: 定義 frontend top navbar、sidebar toggle 位置、系統名稱與 sidebar 分類行為。

### Modified Capabilities

- 無。

## Impact

- 影響範圍：frontend。
- 主要影響檔案：
  - `frontend/src/App.tsx`
  - `frontend/src/App.css`
  - 可能包含 `frontend/src/index.css`
- 不影響 backend。
- 不影響 `/api/health` API contract。
- 不新增 npm dependencies。
