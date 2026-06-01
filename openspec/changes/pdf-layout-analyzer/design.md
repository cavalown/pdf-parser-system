## Context

目前 backend 的 PDF endpoint（`POST /api/pdf/parse`）使用 `pypdf` 進行純文字擷取，無任何版面資訊。要產出「Tailwind 版面規格書」，需要字元級別的座標、字體資訊與表格偵測能力，`pypdf` 無法勝任。

這次變更在現有 FastAPI 分層架構下新增一組獨立的 analyze endpoint + service + schema，不修改現有 parse 功能。

## Goals / Non-Goals

**Goals:**

- 新增 `POST /api/pdf/analyze`，回傳 `LayoutSpec` JSON。
- 以 `pdfplumber`（MIT License）取代 `pypdf` 在 layout 分析上的不足。
- 支援多頁分析，每頁獨立輸出 typography tokens 與 layout blocks。
- 偵測 header/footer（多頁：跨頁重複策略；單頁：位置啟發式）。
- 表格 schema（欄寬、對齊、border、cell padding）嵌入對應 block。

**Non-Goals:**

- 不修改現有 `POST /api/pdf/parse` endpoint 或其 service/schema。
- 不支援掃描式（圖片）PDF——此類 PDF 無可擷取字元，結果為空。
- 不建立 frontend UI。
- 不實作 OCR。

## Decisions

### Decision: 使用 pdfplumber 作為 layout 分析引擎

`pdfplumber`（MIT License）建立在 `pdfminer.six` 之上，提供：
- `page.chars`：每個字元的 `x0`, `top`, `x1`, `bottom`, `fontname`, `size`
- `page.extract_words()`：word-level bbox
- `page.find_tables()`：結構化表格偵測，含欄位座標
- `page.lines`、`page.rects`：線條與矩形（用於 border 偵測）
- `page.mediabox`（`page.width`, `page.height`）：頁面尺寸

替代方案：
- `pymupdf (fitz)`：功能更強，但 AGPL 授權，不符合開源需求。
- `camelot-py`：專注表格擷取，無法做全頁 layout 分析。
- `pdfminer.six` 直接使用：pdfplumber 是其封裝，不需要直接操作低層 API。

### Decision: pdfplumber 座標系統

pdfplumber 使用 **top-left 為原點、y 向下遞增**的座標系（pdfminer 已做轉換）。

- `char['top']`：字元頂端距頁面頂端的距離（pt）
- `char['bottom']`：字元底端距頁面頂端的距離（pt）
- `page.height`：頁面高度（pt）

因此：
- Header 偵測：`block.top < page.height * 0.15`
- Footer 偵測：`block.bottom > page.height * 0.90`

輸出至 `bbox` 時，欄位命名為 `x0`, `top`, `x1`, `bottom`，與 pdfplumber 一致，方便後續工具使用。

### Decision: 分析 pipeline 架構

分五個函式，由 `pdf_analyzer_service.py` 統籌：

```
analyze_pdf(content: bytes) -> LayoutSpec
  ├── _extract_canvas(first_page) -> Canvas
  ├── for each page:
  │     ├── _extract_typography_tokens(page) -> TypographyTokens
  │     ├── _extract_blocks(page, tables) -> list[LayoutBlock]
  │     └── _classify_header_footer(blocks, page_height) → 標記 type
  └── _detect_header_footer_multi_page(all_pages_blocks, page_height)
           → 多頁重複策略，覆寫 type
```

### Decision: Typography token 演算法

1. 統計 `page.chars` 中各字體大小（`round(size, 1)`）的字元數。
2. **body**：出現字元數最多的字體大小。
3. **h1**：該頁最大的字體大小。
4. **label**：h1 與 body 之間的中間層級；若不存在中間層，退而取 body 大小但 fontname 含 `Bold` 的字元。
5. **font weight**：解析 fontname 字串：
   - 含 `Bold`（大小寫皆可）→ `font-bold`
   - 含 `Medium` → `font-medium`
   - 其他 → `font-normal`
6. **text-right 偵測**：若某區塊字元的 `x0` offset ratio（`(x0 - block.x0) / block.width`）中位數 > 0.6，則該 token 加入 `text-right`。

### Decision: Layout block 偵測演算法

1. 以 `page.extract_words(extra_attrs=['fontname', 'size'])` 取得 word bbox。
2. 依 `top` 排序，按 y 方向聚類成「行」（同一行：`|top - prev_top| < 3pt`）。
3. 若連續兩行的間距 > `1.5 × avg_line_height`，切分為新 block。
4. 若 block 的 bbox 與任一 `page.find_tables()` 結果重疊（IoU > 0 即算）→ `type: "table"`。
5. 非 table block：分析 x 軸分佈是否有 gap > `page.width * 0.1`：
   - 有 → `type: "two_column"`，計算左右欄寬比例，輸出 `grid grid-cols-[Xfr_Yfr]`。
   - 無 → `type: "text"`，計算行距，輸出 `flex flex-col space-y-[Xpx]`。
6. 依 `top` 排序，確保 top-to-bottom 輸出。

### Decision: Header/Footer 多頁重複偵測策略

- **First pass**：收集每頁所有 blocks 的 y 中心點（`(top + bottom) / 2 / page.height`，正規化 0–1）。
- **Grouping**：若多頁的 blocks 在正規化 y 中心點 ±0.05 內，視為同一「位置組」。
- **標記邏輯**：
  - 某位置組出現在 > 50% 的頁面 AND 正規化 y 中心點 < 0.15 → 標記為 `header`。
  - 某位置組出現在 > 50% 的頁面 AND 正規化 y 中心點 > 0.90 → 標記為 `footer`。
- **單頁 fallback**：`top < page.height * 0.15` → `header`；`bottom > page.height * 0.90` → `footer`。

### Decision: Table schema 計算

`pdfplumber.Table` 物件提供：
- `bbox`：表格邊界
- `col_positions`：各欄邊界 x 座標清單

欄寬：`[col_positions[i+1] - col_positions[i] for i in range(n-1)]`

欄寬比例（fr 單位）：各欄寬除以最小欄寬後四捨五入，以 GCD 化簡。

對齊偵測：對每欄，取欄內字元的 `(x0 - col_x0) / col_width` offset ratio 中位數：
- < 0.3 → `text-left`
- 0.3–0.6 → `text-center`
- > 0.6 → `text-right`

Border 偵測：在表格 bbox 範圍內搜尋 `page.lines`，若存在水平線 → `has_border: true`。

Cell padding：取儲存格內字元的 `top - cell_top` 與 `cell_bottom - bottom` 平均值，轉換為 px（`1pt ≈ 1.333px`），輸出為 `py-[Xpx]`。

### Decision: 單位轉換規則

| 用途 | 單位 | 範例 |
|---|---|---|
| 頁面尺寸 | mm | `w-[210mm] h-[297mm]` |
| 頁面 padding（邊距） | mm | `p-[20mm]` |
| 字體大小 | pt | `text-[10pt]` |
| 行距、元件間距 | px | `space-y-[12px]` |
| Grid gap | px | `gap-[20px]` |
| Cell padding | px | `py-[8px] px-[6px]` |

換算：`1pt = 1.333px`；`1mm = 2.835pt`。

## Risks / Trade-offs

- [Risk] pdfplumber 的 `find_tables()` 對無格線表格（依靠文字對齊推斷）偵測率不穩定。→ Mitigation：加入 `table_settings` 調整偵測策略；未偵測到表格時，該 block 降級為 `type: "text"`。
- [Risk] 字體大小的 label/h1/body 分層依賴頁面字型種類豐富程度，若某頁只有一種字體大小，三個 token 將相同。→ Mitigation：允許 token 相同，消費端（AI agent）自行忽略重複 token。
- [Risk] 多頁跨頁重複偵測若頁數過少（2 頁），50% 閾值意為只要 1 頁相同就標記。→ Mitigation：可接受；2 頁文件仍可正確辨識 header/footer。
- [Risk] 中文 PDF 的 fontname 通常包含 Unicode 編碼前綴（如 `ABCDEF+NotoSansCJK-Bold`），bold 關鍵字仍在名稱末段。→ Mitigation：比對時使用 case-insensitive 字串包含，不依賴固定位置。
- [Risk] pdfplumber 分析大型 PDF 時可能速度較慢。→ Mitigation：目前為同步處理，可接受；未來若需要可改為 background task。

## Open Questions

- 若 PDF 為加密文件（pdfplumber 無法開啟），應回傳 400 還是 422？目前設計以 HTTP 500 讓 FastAPI 通用 error handler 接管，待確認是否需要明確攔截。
- 欄寬比例的 fr 化簡是否有上限？（例如若 GCD 為 1，欄位比例為 37fr_13fr 是否太細？）可設定最大精度為 12 分格。
