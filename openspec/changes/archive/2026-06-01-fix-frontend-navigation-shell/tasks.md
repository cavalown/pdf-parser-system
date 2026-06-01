## 1. Frontend

- [x] 1.1 更新 `frontend/src/App.tsx` 的 app shell 結構，加入 top navbar 並將品牌文字改為 `PDF Fac.`。
- [x] 1.2 將 `PDF Fac.` 設為 home link，點擊後導向 `/`。
- [x] 1.3 調整 sidebar toggle button 的 DOM 位置，使 menu icon 位於 navbar 下方的 sidebar 區域。
- [x] 1.4 將 sidebar navigation items 改為 `PDF Analyze`、`PDF Modify`、`Setting`。
- [x] 1.5 保留 sidebar expanded/collapsed state，並確認收合後仍顯示 category icons。
- [x] 1.6 保留 collapsed sidebar hover/focus label，並對應顯示 `PDF Analyze`、`PDF Modify`、`Setting`。
- [x] 1.7 確認首頁 `/api/health` 檢查與 service status rendering 行為未被移除。

## 2. Validation

- [x] 2.1 執行 frontend lint，確認 React、TypeScript 與 ESLint 規則通過。
- [x] 2.2 執行 frontend build，確認 production build 通過。
- [x] 2.3 以本機 dev server 檢查 navbar、sidebar 展開/收合、hover/focus label 與首頁 health status。
