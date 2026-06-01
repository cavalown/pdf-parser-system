# 新增服務存活檢查與前端 Dashboard Shell

## 背景

目前前端需要知道 backend API server 是否仍然存活，並需要一個可收合的側邊欄作為後續 PDF parser 功能的操作入口。

## 目標

- Backend 提供可供 frontend 檢查服務存活的 API。
- Frontend 首頁串接服務存活 API，顯示目前連線狀態。
- Frontend 建立 top navbar，左上方顯示系統名稱 `PDF Fac.`，點擊可回首頁。
- Frontend 建立左側 sidebar，可用 menu icon 收合。
- Menu icon 位於 top navbar 內，並緊鄰 `PDF Fac.` 左側。
- Sidebar 分類為 `PDF Analyze`、`PDF Modify`、`Setting`。
- Sidebar 收合後保留 icon，並在 hover 或 focus 時顯示功能名稱。
- Frontend 建立紅色與黑色為基底的 design system。

## 影響範圍

- shared：新增 `/api/health` API contract。
- backend：NestJS `AppController` 與 `AppService` 回傳服務存活資訊。
- frontend：React 首頁、top navbar、sidebar app shell、Vite dev proxy 與全域 CSS tokens。

## Impact

- API contract：
  - `GET /api/health`
  - 回傳 JSON object，包含 `alive`、`status`、`service`、`checkedAt`。
- Frontend local development：
  - Vite dev server 透過 `/api` proxy 轉發到 `http://127.0.0.1:3000`。
- 無新增 npm dependencies。
