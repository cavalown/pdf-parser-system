# Frontend Rules

這份文件記錄 frontend 專屬規範。

## Stack

- Frontend 使用 React、Vite、TypeScript。
- UI library 使用 MUI (Material UI)。

## UI 與 Components

- 開發所有 UI 元件時，優先使用 MUI 既有 components。
- 只有在 MUI 無法滿足需求時，才自行撰寫新的 component。
- 自行撰寫 component 時，也必須遵循 MUI 的 style、theme 與互動慣例。
- UI 實作應與既有 components 和 styles 保持一致。
- 除非能解決實際專案需求，避免新增大型 UI dependencies。
