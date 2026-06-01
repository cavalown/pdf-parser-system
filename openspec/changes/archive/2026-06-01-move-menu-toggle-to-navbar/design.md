## Context

目前 frontend navigation shell 已有 top navbar、`PDF Fac.` brand link、左側 sidebar、以及 sidebar expanded/collapsed state。現行實作將 menu icon 放在 sidebar 上方控制列；新的需求是將 menu icon 移到 navbar 內，並放在 `PDF Fac.` 左邊。

這個變更只調整 frontend layout 與互動位置，不改 sidebar 分類、不改 health check、不改 backend API。

## Goals / Non-Goals

**Goals:**

- 將 menu icon 移入 top navbar。
- 讓 menu icon 立即位於 `PDF Fac.` brand link 左邊。
- 保留 menu icon 控制 sidebar expanded/collapsed 的行為。
- 保留 `PDF Fac.` 作為 home link。
- 保留 sidebar 分類 `PDF Analyze`、`PDF Modify`、`Setting`。

**Non-Goals:**

- 不新增 router 或頁面。
- 不修改 sidebar 分類內容。
- 不修改首頁 health status。
- 不修改 backend 或 `/api/health` API contract。
- 不新增 dependencies。

## Decisions

### Decision: Navbar 承載 menu toggle 與 brand link

Top navbar SHALL 以水平排列呈現：

```txt
top-navbar
└── navbar-left
    ├── menu toggle
    └── PDF Fac. home link
```

理由：
- menu toggle 是全域 shell control，放在 navbar 比放在 sidebar 內更符合使用者目前期望。
- `PDF Fac.` 仍維持 navbar 左上方的主要 brand signal。
- 這讓 sidebar 更專注於功能分類。

替代方案：
- 保留 menu icon 在 sidebar 內並調整對齊。這已不符合新的需求。

### Decision: Navbar 使用暗紅色背景

Top navbar SHALL 使用暗紅色背景，作為 app shell 的主要品牌色區塊。

理由：
- 使用者明確指定 navbar 使用暗紅色。
- 暗紅色延續既有紅黑 design system，同時比純黑 navbar 更能凸顯品牌區域。
- 暗紅色可讓白色或淺色 `PDF Fac.` 文字與 menu icon 維持清楚對比。

替代方案：
- 使用目前 near-black navbar，只在 active states 使用紅色。這不符合新的視覺需求。

### Decision: Sidebar state 保留在 App component

既有 `sidebarOpen` state SHALL 繼續留在 `App.tsx`，只是由 navbar 裡的 button 觸發。

理由：
- 目前 app 尚未拆成獨立 layout components。
- 這是位置調整，不需要新增 state management 或拆檔。

替代方案：
- 拆出 `Navbar` 與 `Sidebar` components 並透過 props 傳遞 state。這較利於未來擴充，但本次變更範圍很小，會增加不必要抽象。

### Decision: Sidebar 不再包含 toggle control row

Sidebar SHALL 只保留 navigation list，不再保留 sidebar control row。

理由：
- 避免畫面上出現兩個 menu toggle。
- 保持 sidebar 為功能導覽容器。

替代方案：
- Navbar 和 sidebar 兩邊都保留 toggle。這會造成互動重複，且不符合需求。

## Risks / Trade-offs

- [Risk] Navbar 左側元素變多，窄螢幕可能擁擠。 → Mitigation：menu button 使用固定 icon button 尺寸，brand text 使用穩定字級與不換行設定。
- [Risk] 暗紅色 navbar 若與紅色 accent 過近，可能降低層次。 → Mitigation：使用較深的 red tone 作為 navbar background，保留較亮 red 作為 hover/focus accent。
- [Risk] Toggle 從 sidebar 移出後，sidebar 收合狀態下使用者可能需要視覺連結知道按鈕控制 sidebar。 → Mitigation：維持 `aria-expanded` 與清楚的 menu icon 位置；navbar 左側靠近 sidebar 起點。
- [Risk] 若 CSS 只移 DOM 不清理 `.sidebar-control`，會留下無用樣式。 → Mitigation：實作時移除或停用不再使用的 sidebar control CSS。
