# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 工作規則

- 永遠使用正體中文撰寫文件與回覆使用者，專有名詞與技術名詞維持英文。
- AI agent 永遠不主動執行 git 操作；需要 git 相關操作時，必須先由使用者明確要求。
- 新增 pattern 前，優先沿用既有專案結構與慣例。
- 變更範圍應聚焦在目前要求的 feature 或 fix。
- 沒有明確理由時，不要重寫無關檔案或大範圍重新格式化。
- 完成工作前，執行最相關的 build 或 lint 指令。
- 新增或修改 API 後，執行 `export_openapi.py` 更新 `openspec/openapi.json`。

## 開發指令

### Frontend（`frontend/`）

```bash
npm install
npm run dev       # http://localhost:5173
npm run build     # tsc + vite build
npm run lint
```

### Backend（`backend/`）

```bash
source venv/bin/activate
pip install -r requirements.txt
python main.py    # http://localhost:3000
```

OpenAPI spec 更新：

```bash
cd backend
python export_openapi.py   # 輸出至 openspec/openapi.json
```

## Stack

- **Frontend**: React 19, Vite, TypeScript。UI library 規劃使用 MUI（目前尚未安裝）。
- **Backend**: Python, FastAPI, uvicorn, pypdf, pydantic-settings。venv 在 `backend/venv/`。

## 架構

### Frontend

目前以單一 `App.tsx` 組成，包含 top navbar、collapsible sidebar 與 main content。Vite dev server 將 `/api/*` proxy 至 `http://127.0.0.1:3000`，因此 frontend 直接呼叫 `/api/...` 即可，無需寫死 backend URL。

### Backend

FastAPI 分層架構：

```
app/
  main.py               FastAPI app，掛載 CORS middleware，router prefix = /api
  core/config.py        pydantic-settings，讀取 .env（APP_NAME, DEBUG）
  api/router.py         彙整所有 endpoint routers
  api/endpoints/        HTTP 層，只處理 request/response，呼叫 services
  services/             業務邏輯（例：pdf_service.py 用 pypdf 解析）
  schemas/              Pydantic BaseModel，request/response schema
```

新增 endpoint 時：在 `endpoints/` 建檔 → 在 `services/` 實作邏輯 → 在 `schemas/` 定義 model → 在 `router.py` 掛載。每個 endpoint 必須設定 `response_model`、`summary`、`description`。

### OpenSpec

`openspec/` 存放 spec-driven 開發文件：

```
openspec/
  config.yaml     project context 與各 artifact 的撰寫規則
  openapi.json    由 export_openapi.py 自動產生，勿手動修改
  specs/          已確認的 system behavior source of truth
  changes/        進行中的 change proposals（含 proposal、specs、design、tasks）
    archive/      已完成封存的 changes
```

新功能開發流程：`/openspec-propose <slug>` 起草 proposal → `/openspec-spec <slug>` 撰寫 spec。
