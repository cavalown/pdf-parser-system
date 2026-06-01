## Context

目前 frontend 使用 React + Vite + TypeScript，主畫面由 `App.tsx` 同時承載 app shell、top navbar、sidebar、首頁 `/api/health` 呼叫，以及 `PDF Analyze`、`PDF Modify`、`Setting` 的 placeholder 區塊。sidebar 目前以同頁錨點移動，並不代表真正的頁面邊界。

這次變更的核心是資訊架構調整：讓 app shell 成為穩定 layout，讓 sidebar 每個分類對應各自 page component，並讓首頁維持單純的 backend 連線狀態頁。backend health API contract 不變。

## Goals / Non-Goals

**Goals:**

- 建立 route-based frontend page structure。
- 將 layout shell 與 page content 分離，避免首頁 component 持續膨脹。
- 讓 sidebar item 對應穩定 route，並依照目前 route 顯示 active state。
- 將首頁拆成獨立 `HomePage`，只顯示 backend 連線狀態、service metadata、錯誤狀態與重新檢查操作。
- 建立 `PDF Analyze`、`PDF Modify`、`Setting` 的獨立 page component 與基本空狀態。
- 保留既有 top navbar、`PDF Fac.` home link、sidebar collapsed/expanded、collapsed hover/focus label 與紅黑視覺系統。

**Non-Goals:**

- 不實作 PDF analyze workflow。
- 不實作 PDF modify workflow。
- 不實作 settings form 或 persistence。
- 不修改 backend API 或 `/api/health` response。
- 不進行整套 UI framework migration。

## Decisions

### Decision: 使用 `react-router-dom` 建立 route-based pages

Frontend 將導入 `react-router-dom`，使用 browser route 將 `/`、`/analyze`、`/modify`、`/settings` 對應到獨立 page component。

理由：
- 使用者明確希望 sidebar 每個項目都是各自一頁 component，route 是最清楚且可維護的頁面邊界。
- URL 可分享、可重新整理，也能自然支援 browser history。
- active sidebar item 可由 current location 推導，不需要維護額外 duplicated state。

替代方案：
- 使用 local state 切換 page。這能避免新增 dependency，但會讓 URL 不反映目前頁面，重新整理會回到首頁，長期比較像 tabs 而不是 pages。

### Decision: `App` 保留 routing provider，`AppShell` 負責 layout

建議將結構切成：

```txt
App
└── BrowserRouter
    └── Routes
        └── AppShell
            ├── TopNavbar
            ├── Sidebar
            └── Outlet
                ├── HomePage
                ├── PdfAnalyzePage
                ├── PdfModifyPage
                └── SettingPage
```

理由：
- `AppShell` 可以專注在 navbar、sidebar、collapse state 與主要內容容器。
- page components 各自擁有自己的 data fetching 與 UI state，後續功能擴充時不會互相耦合。
- `Outlet` pattern 是 React Router 常見做法，符合可維護 layout route 結構。

替代方案：
- 在 `App.tsx` 手動組合所有 component。這可以更快完成，但會保留目前單檔膨脹問題。

### Decision: 首頁 health check data fetching 留在 `HomePage`

`/api/health` 呼叫、loading/error 狀態、refresh 操作與 service metadata 顯示都應位於 `HomePage` 或其附近的 helper hook/function，不放在 `AppShell`。

理由：
- health status 是首頁內容，不是全域 layout 狀態。
- 後續 `PDF Analyze` 與 `PDF Modify` 會有自己的資料流，將 page data 放在 page 邊界內比較容易維護。

替代方案：
- 將 health status 放在 shell 或 navbar 作為全域狀態。這會改變目前首頁用途，也會讓 shell 承擔過多 page-specific 行為。

### Decision: 不在本變更導入 MUI migration

專案規範偏好 MUI，但目前 frontend 既有 implementation 仍是 custom CSS，`package.json` 也尚未安裝 MUI。這次變更主要是 routing 與 component boundary，不新增複雜 UI primitives；實作時應沿用既有 CSS token 與 visual pattern。

理由：
- 同時導入 router 與 MUI migration 會擴大變更範圍。
- 現有 sidebar、navbar、status panel 已可支撐本次需求。
- 未來若要導入 MUI theme，應另開 change 處理 dependency、theme provider 與 component migration。

替代方案：
- 這次一併安裝 MUI 並改寫 shell components。這符合長期 UI library 規範，但會把資訊架構變更與 UI framework migration 綁在一起，驗證成本較高。

## Risks / Trade-offs

- [Risk] 新增 `react-router-dom` 會增加 dependency 與 routing 設定成本。→ Mitigation：僅使用標準 browser routing、layout route 與 `NavLink`/location active state，避免自訂 routing abstraction。
- [Risk] Vite dev server history fallback 與 production hosting rewrite 需要支援 browser route refresh。→ Mitigation：本地 Vite 可處理 fallback；部署時若加入 static hosting，需設定 fallback 到 `index.html`。
- [Risk] 現有 archived spec 曾將 router 列為 non-goal。→ Mitigation：本 change 明確改變 scope，將「各 sidebar 項目是獨立頁面」列為新的產品需求。
- [Risk] 暫不導入 MUI 會與 frontend 長期規範有落差。→ Mitigation：本次只重整 route/page boundary，不新增大型 UI component；MUI migration 另行規劃。
- [Risk] 空狀態頁面可能被誤認為功能完成。→ Mitigation：`PDF Analyze`、`PDF Modify`、`Setting` 頁面文案應明確表達目前是頁面入口或尚未設定內容，不提供假互動。

## Migration Plan

1. 新增 routing dependency 並在 `App` 設定 `BrowserRouter` 與 routes。
2. 拆出 app shell、navbar、sidebar 與 page components。
3. 將首頁 health check UI 與 request state 移入 `HomePage`。
4. 將 sidebar links 從 hash anchors 改為 route links，並加入 route-aware active state。
5. 移除首頁中的 `PDF Analyze`、`PDF Modify`、`Setting` placeholder 區塊。
6. 執行 frontend lint/build，並以瀏覽器檢查 route navigation、refresh、sidebar collapse 與首頁 health status。

Rollback 策略：若 routing 導入造成阻塞，可暫時回復為單一 `App.tsx` hash anchor navigation；因 backend API 不變，rollback 不需要資料或 API migration。

## Open Questions

- 未來 production hosting 會使用哪種 static server 或 reverse proxy？部署時需要確認 non-root route refresh 是否 fallback 到 `index.html`。
- `PDF Analyze`、`PDF Modify`、`Setting` 的最終資訊架構是否會包含子路由？本變更先只建立 top-level page。
