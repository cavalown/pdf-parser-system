## 1. Backend 依賴

- [x] 1.1 在 `backend/requirements.txt` 新增 `pdfplumber>=0.11.0`。

## 2. Backend Schema

- [x] 2.1 建立 `backend/app/schemas/pdf_analyze.py`，定義以下 Pydantic models：`BBox`、`TableSchema`、`LayoutBlock`、`TypographyTokens`、`PageAnalysis`、`Canvas`、`LayoutSpec`。

## 3. Backend Service

- [x] 3.1 建立 `backend/app/services/pdf_analyzer_service.py`，實作 `_extract_canvas(page)` 函式：讀取 pdfplumber page 的 width/height，識別 A4/Letter/Custom，推算邊距並輸出 `tailwind_page_class`。
- [x] 3.2 實作 `_infer_font_weight(fontname: str) -> str`：依 fontname 字串回傳 `font-bold`、`font-medium` 或 `font-normal`。
- [x] 3.3 實作 `_extract_typography_tokens(page) -> TypographyTokens`：統計字元大小頻率，識別 body/h1/label 三級，輸出 Tailwind class 字串。
- [x] 3.4 實作 `_extract_blocks(page, tables) -> list[LayoutBlock]`：將 words 依 y 方向聚類成行再聚類成 block，偵測 text/two_column/table 類型，計算 `tailwind_layout`，輸出帶 `bbox` 的 block 清單（top-to-bottom 排序）。
- [x] 3.5 實作 `_classify_header_footer_single_page(blocks, page_height) -> list[LayoutBlock]`：單頁啟發式，`top < page_height * 0.15` → header，`bottom > page_height * 0.90` → footer。
- [x] 3.6 實作 `_detect_header_footer_multi_page(pages_blocks, page_height) -> list[list[LayoutBlock]]`：跨頁重複偵測，正規化 y 中心點 ±0.05 聚類，出現在 > 50% 頁面的區域標記為 header/footer。
- [x] 3.7 實作 `_extract_table_schema(table, page) -> TableSchema`：計算欄寬、fr 比例、欄位對齊（offset ratio）、border（page.lines 比對）、cell padding。
- [x] 3.8 實作主函式 `analyze_pdf(content: bytes) -> LayoutSpec`：串接以上函式，回傳完整 `LayoutSpec`。

## 4. Backend Endpoint

- [x] 4.1 建立 `backend/app/api/endpoints/pdf_analyze.py`，定義 `POST /analyze` router，接受 PDF upload，呼叫 `analyze_pdf`，設定 `response_model=LayoutSpec`、`summary`、`description`。非 PDF 檔案回傳 HTTP 400。
- [x] 4.2 在 `backend/app/api/router.py` 掛載 `pdf_analyze` router，prefix 為 `/pdf`，使 endpoint 路徑為 `POST /api/pdf/analyze`。

## 5. OpenAPI Spec 更新

- [x] 5.1 執行 `cd backend && python export_openapi.py`，確認 `openspec/openapi.json` 新增 `POST /api/pdf/analyze`。

## 6. Validation

- [x] 6.1 安裝依賴：`source backend/venv/bin/activate && pip install -r backend/requirements.txt`，確認 `pdfplumber` 安裝成功。
- [x] 6.2 啟動 backend server，對 `POST /api/pdf/analyze` 上傳一份電腦產生的 PDF，確認回傳 HTTP 200 與有效的 `LayoutSpec` JSON。
- [x] 6.3 對 `POST /api/pdf/analyze` 上傳非 PDF 檔案，確認回傳 HTTP 400。
