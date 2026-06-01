# Tasks

## Backend

- [x] 新增或更新服務存活 API 回應欄位，包含 `alive`、`status`、`service`、`checkedAt`。
- [x] 維持 NestJS controller/service 分層。
- [x] 執行 backend build 驗證。

## Frontend

- [x] 建立可收合的左側 sidebar。
- [x] Sidebar 收合後只顯示 icon，並支援 hover/focus 顯示 label。
- [x] 建立紅黑基底 CSS design tokens 與主要 layout。
- [x] 首頁串接 `/api/health` 並顯示存活狀態。
- [x] 設定 Vite `/api` dev proxy。
- [x] 執行 frontend lint 與 build 驗證。
- [x] 將系統名稱修正為 `PDF Fac.`。
- [x] 建立 top navbar，並將 `PDF Fac.` 放在 navbar 左上方且點擊回首頁。
- [x] 將 menu icon 移到 top navbar 內，並放在 `PDF Fac.` 左側。
- [x] 將 sidebar 分類修正為 `PDF Analyze`、`PDF Modify`、`Setting`。
- [x] 重新執行 frontend lint 與 build 驗證。

## Shared

- [x] 定義 frontend 與 backend 共用的 `/api/health` response contract。
- [x] 使用 Vite proxy 驗證 frontend local URL 可取得 backend health response。
