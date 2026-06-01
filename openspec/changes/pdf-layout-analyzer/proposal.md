## Why

目前 backend 的 PDF 功能（`POST /api/pdf/parse`）只能擷取純文字，無法提供任何版面資訊。若要透過 AI agent 將 PDF 的視覺版型重現為 Vue + Tailwind 畫面，需要一份從 PDF 榨出的「Tailwind 規格書」，包含頁面尺寸、字體階層、區塊佈局與表格結構。

## What Changes

- 新增 `POST /api/pdf/analyze` endpoint，接受 PDF 檔案上傳，回傳 Tailwind 版面規格 JSON。
- 新增 `pdfplumber`（MIT License）作為 layout 分析依賴，取代 `pypdf` 在此功能上的不足——`pypdf` 只能擷取文字，`pdfplumber` 能提供字元座標、字體資訊與表格偵測。
- 分析範疇涵蓋 4 個核心領域：
  1. **Canvas**：頁面實體尺寸（A4/Letter/Custom）、推算邊距，輸出 `tailwind_page_class`。
  2. **Typography Tokens**（per-page）：從字元資料聚類出 h1/label/body 三級字體規格，包含字體大小、字重、對齊方式，輸出 Tailwind class 字串。
  3. **Layout Blocks**（精確偵測）：以垂直間距聚類出每個視覺區塊，偵測 header/footer/text/two_column/table 等類型，計算分欄比例，輸出 `tailwind_layout`。
  4. **Table Schema**（嵌入 block）：偵測表格欄數、欄寬、每欄對齊方式、有無橫線與儲存格內距。
- Header/Footer 偵測策略：多頁時以跨頁相同 y 位置重複出現的區塊判定；單頁時以位置啟發式（上方/下方 12%）判定。
- 分析結果以頁為單位巢狀輸出，每個 block 附帶 `bbox`（PDF 座標, pt）供 AI agent 理解相對位置。

## Capabilities

### New Capabilities

- `backend-pdf-layout-analyzer`：定義 `POST /api/pdf/analyze` endpoint、pdfplumber 分析 pipeline、以及回傳 Tailwind 版面規格 JSON 的完整行為與 response schema。

## Impact

- **Backend**：新增 `app/api/endpoints/pdf_analyze.py`、`app/services/pdf_analyzer_service.py`、`app/schemas/pdf_analyze.py`，並在 `app/api/router.py` 掛載新 router。
- **Dependencies**：新增 `pdfplumber`（MIT License）至 `backend/requirements.txt`。
- **API Contract**：新增 `POST /api/pdf/analyze`，回傳 `LayoutSpec` schema（詳見 capability spec）。現有 `POST /api/pdf/parse` contract 不變。
- **Frontend**：此 change 不涉及 frontend 變更。
- **Shared**：不影響現有 shared spec。
