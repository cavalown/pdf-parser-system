# Codex 專案指南

這份文件是 Codex 和其他 AI coding agents 的本地專案指南。當專案規則、架構、工作流程或 specs 有變更時，請同步更新這份文件。

## 專案

`pdf-parser-system` 用來解析 PDF 檔案，並預覽擷取後的內容。

目前結構：

```txt
pdf-parser-system/
  frontend/   React + Vite frontend
  backend/    NestJS API server
  ai/         給 AI 使用的 rules、skills、specs 和專案筆記
```

## AI 目錄

使用 `ai/` 存放未來 AI-assisted work 需要遵循的專案知識。

目前結構：

```txt
ai/
  codex.md        主要指令與專案指南
  rules/
    shared.md     全專案共通工程規則
    frontend.md   Frontend 專屬規則
    backend.md    Backend 專屬規則
  skills/
    shared/       共通工作流程或領域程序
    frontend/     Frontend 專屬工作流程
    backend/      Backend 專屬工作流程
  specs/
    shared/       跨 frontend/backend 的 specs 與 API contract
    frontend/     Frontend specs、UI/UX 與互動流程
    backend/      Backend specs、API 與處理流程
```

讀取專案規範時，請優先查看：

- `ai/rules/shared.md`
- `ai/rules/frontend.md`
- `ai/rules/backend.md`

## OpenSpec

本專案已初始化 OpenSpec。

OpenSpec 結構：

```txt
openspec/
  config.yaml       OpenSpec project context 與 per-artifact rules
  specs/            目前已存在的 system behavior source of truth
  changes/          proposed changes
    archive/        已完成並封存的 changes
```

OpenSpec slash commands 已設定給 Codex，可使用：

- `/opsx:propose`
- `/opsx:explore`
- `/opsx:apply`
- `/opsx:archive`

使用 OpenSpec 時，仍必須遵守 `ai/rules/` 內的專案規範。

## 開發指令

Frontend:

```bash
cd frontend
npm install
npm run dev
npm run build
npm run lint
```

Backend:

```bash
cd backend
npm install
npm run start:dev
npm run build
npm test
npm run lint
```

預設本機 URLs：

```txt
frontend: http://localhost:5173
backend:  http://localhost:3000
health:   http://localhost:3000/api/health
```

## 工作規則

- 永遠使用正體中文撰寫文件與回覆使用者，專有名詞與技術名詞維持英文。
- 全專案都使用 TypeScript。
- 所有建議與實作方向，應以專業化、業界常用、可維護的方式為依據。
- AI agent 永遠不主動執行 git 操作；需要 git 相關操作時，必須先由使用者明確要求。
- 新增 pattern 前，優先沿用既有專案結構與慣例。
- 變更範圍應聚焦在目前要求的 feature 或 fix。
- 沒有明確理由時，不要重寫無關檔案或大範圍重新格式化。
- 當行為有變更時，新增或更新聚焦的 tests。
- 完成工作前，執行最相關的 build、lint 或 test 指令。
- 影響後續實作的長期決策，應記錄在 `ai/`。

## Frontend 筆記

- Stack: React, Vite, TypeScript.
- UI library: MUI (Material UI).
- 開發 UI 元件時，優先使用 MUI 既有 components；自行撰寫 component 時，也必須遵循 MUI 的 style、theme 與互動慣例。
- UI 實作應與既有 components 和 styles 保持一致。
- 除非能解決實際專案需求，避免新增大型 UI dependencies。

## Backend 筆記

- Stack: NestJS, TypeScript.
- Backend API 都需要提供 property 說明與 controller 說明。
- API behavior 應保持明確，並在可行時以聚焦 tests 覆蓋。
- 使用 NestJS module、provider、controller 和 service patterns，避免 ad hoc structure。

## 待釐清問題

- PDF parsing library 和 extraction strategy 尚未定義。
- File upload flow 和 storage rules 尚未定義。
- 擷取後 PDF content 的 output schema 尚未定義。
