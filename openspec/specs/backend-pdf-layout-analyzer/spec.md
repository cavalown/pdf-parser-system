## Requirements

### Requirement: PDF layout analysis endpoint

Backend SHALL expose `POST /api/pdf/analyze` that accepts a PDF file upload and returns a `LayoutSpec` JSON response describing the Tailwind layout specification extracted from the document.

#### Scenario: 成功分析多頁 PDF

- **GIVEN** backend 正常運作
- **WHEN** client 送出 `POST /api/pdf/analyze` 並附上一份電腦產生的多頁 PDF
- **THEN** backend SHALL return HTTP 200 with a `LayoutSpec` JSON body
- **AND** `LayoutSpec.pages` SHALL contain one entry per page in the PDF
- **AND** each page entry SHALL contain `page`（頁碼，從 1 起算）、`typography_tokens`、`blocks`

#### Scenario: 上傳非 PDF 檔案

- **GIVEN** backend 正常運作
- **WHEN** client 送出 `POST /api/pdf/analyze` 並附上非 PDF 檔案（如 `.png`、`.docx`）
- **THEN** backend SHALL return HTTP 400
- **AND** response body SHALL contain 錯誤說明

---

### Requirement: Canvas spec 擷取

Backend SHALL extract page dimensions from the PDF mediabox and generate a `canvas` object containing page size classification, physical dimensions in points, and a `tailwind_page_class` string.

#### Scenario: 識別 A4 頁面

- **GIVEN** PDF 頁面 mediabox 寬度約為 595 pt、高度約為 842 pt（誤差 ±5 pt）
- **WHEN** backend 執行 canvas 分析
- **THEN** `canvas.size` SHALL be `"A4"`
- **AND** `canvas.tailwind_page_class` SHALL contain `w-[210mm]` 與 `h-[297mm]`

#### Scenario: 識別 Letter 頁面

- **GIVEN** PDF 頁面 mediabox 寬度約為 612 pt、高度約為 792 pt（誤差 ±5 pt）
- **WHEN** backend 執行 canvas 分析
- **THEN** `canvas.size` SHALL be `"Letter"`
- **AND** `canvas.tailwind_page_class` SHALL contain `w-[216mm]` 與 `h-[279mm]`

#### Scenario: 識別非標準頁面尺寸

- **GIVEN** PDF 頁面 mediabox 不符合 A4 或 Letter 標準尺寸
- **WHEN** backend 執行 canvas 分析
- **THEN** `canvas.size` SHALL be `"Custom"`
- **AND** `canvas.width_pt` 與 `canvas.height_pt` SHALL reflect actual mediabox values

#### Scenario: 推算頁面邊距

- **GIVEN** PDF 頁面含有可擷取文字
- **WHEN** backend 以所有字元 bbox 的 x0 中位數推算 left margin
- **THEN** `canvas.tailwind_page_class` SHALL include a padding class（如 `p-[20mm]` 或 `px-[20mm] py-[25mm]`）reflecting the inferred margins

---

### Requirement: Per-page typography tokens 擷取

Backend SHALL analyze character-level font data on each page and output three typography token levels—`h1`、`label`、`body`—as Tailwind class strings, per page.

#### Scenario: 識別 body 字體（最高頻率字體大小）

- **GIVEN** 某頁含有多種字體大小的字元
- **WHEN** backend 統計各字體大小的出現字元數
- **THEN** `typography_tokens.body` SHALL be based on the most frequently occurring font size on that page
- **AND** `typography_tokens.body` SHALL be a Tailwind class string（如 `"text-[10pt] font-normal text-slate-600"`）

#### Scenario: 識別 h1 字體（最大字體大小）

- **GIVEN** 某頁含有多種字體大小的字元
- **WHEN** backend 找出該頁最大的字體大小
- **THEN** `typography_tokens.h1` SHALL be based on the largest font size found on that page
- **AND** font weight SHALL be inferred from font name（包含 `"Bold"` 或 `"bold"` → `font-bold`）

#### Scenario: 識別 label 字體（中間層級）

- **GIVEN** 某頁的字體大小分佈中，h1 與 body 之間存在明顯的中間層級
- **WHEN** backend 找出介於 h1 與 body 之間的字體大小，或 body 大小但 font name 含 Bold
- **THEN** `typography_tokens.label` SHALL reflect that intermediate font level
- **AND** `typography_tokens.label` SHALL be a Tailwind class string（如 `"text-[11pt] font-semibold text-slate-700"`）

#### Scenario: Font name 對應 font weight

- **GIVEN** 一個字元的 font name 包含 `"Bold"` 或 `"bold"` 字串
- **WHEN** backend 產生 typography token
- **THEN** 對應 token SHALL include `font-bold`

- **GIVEN** 一個字元的 font name 包含 `"Medium"` 字串
- **WHEN** backend 產生 typography token
- **THEN** 對應 token SHALL include `font-medium`

- **GIVEN** 一個字元的 font name 不包含上述關鍵字
- **WHEN** backend 產生 typography token
- **THEN** 對應 token SHALL include `font-normal`

#### Scenario: 偵測靠右對齊文字

- **GIVEN** 某頁某區塊的文字 x0 座標普遍接近該區塊右側（offset ratio > 0.6）
- **WHEN** backend 分析字元水平分佈
- **THEN** 對應 typography token SHALL include `text-right`

---

### Requirement: Layout block 精確偵測

Backend SHALL group characters spatially into discrete visual blocks per page, classify each block's type, and generate a `tailwind_layout` string representing its layout pattern.

#### Scenario: 垂直堆疊單欄區塊

- **GIVEN** 某頁有一組字元在 x 軸分佈無明顯斷點，且連續行間距均勻
- **WHEN** backend 執行 block 偵測
- **THEN** 該區塊 SHALL have `type: "text"`
- **AND** `tailwind_layout` SHALL include `flex flex-col`
- **AND** `tailwind_layout` SHALL include 對應行距的 `space-y-[Xpx]`

#### Scenario: 左右並排雙欄區塊

- **GIVEN** 某頁同一 y 範圍內，x 軸出現寬度 > 10% 頁寬的水平空白斷點，將文字分為兩組
- **WHEN** backend 偵測到雙欄分佈
- **THEN** 該區塊 SHALL have `type: "two_column"`
- **AND** `tailwind_layout` SHALL include `grid`
- **AND** `tailwind_layout` SHALL include `grid-cols-[Xfr_Yfr]` reflecting the column width ratio
- **AND** `tailwind_layout` SHALL include `gap-[Xpx]` reflecting the gap between columns

#### Scenario: Block bbox 座標

- **GIVEN** backend 偵測到任一 block
- **WHEN** backend 產生 block 物件
- **THEN** `block.bbox` SHALL contain `x0`, `y0`, `x1`, `y1` in PDF points
- **AND** bbox SHALL tightly bound all characters within the block

#### Scenario: Block 排序

- **GIVEN** 某頁有多個 blocks
- **WHEN** backend 產生 `blocks` 陣列
- **THEN** blocks SHALL be ordered top-to-bottom by `bbox.y1`（視覺閱讀順序）

---

### Requirement: Header 與 Footer 偵測

Backend SHALL identify header and footer blocks on each page and assign them `type: "header"` or `type: "footer"` respectively.

#### Scenario: 多頁跨頁重複區塊識別為 header

- **GIVEN** PDF 有 2 頁以上
- **WHEN** 某個 y 範圍（相對頁面頂端 15% 內）的 block 在超過 50% 的頁面中以相似位置重複出現
- **THEN** 該 block 在每一頁 SHALL have `type: "header"`

#### Scenario: 多頁跨頁重複區塊識別為 footer

- **GIVEN** PDF 有 2 頁以上
- **WHEN** 某個 y 範圍（相對頁面底端 10% 內）的 block 在超過 50% 的頁面中以相似位置重複出現
- **THEN** 該 block 在每一頁 SHALL have `type: "footer"`

#### Scenario: 單頁 PDF 以位置啟發式識別 header/footer

- **GIVEN** PDF 只有 1 頁
- **WHEN** backend 偵測 block 位置
- **THEN** blocks whose `bbox.y1` falls within the top 15% of the page SHALL have `type: "header"`
- **AND** blocks whose `bbox.y0` falls within the bottom 10% of the page SHALL have `type: "footer"`

---

### Requirement: Table schema 擷取（嵌入 block）

Backend SHALL detect tables using pdfplumber's table detection, classify those blocks as `type: "table"`, and embed a `schema` object containing column structure and style information.

#### Scenario: 偵測表格並嵌入 schema

- **GIVEN** 某頁含有結構化表格（有明確格線或對齊欄位）
- **WHEN** pdfplumber 成功偵測到表格
- **THEN** 對應 block SHALL have `type: "table"`
- **AND** `block.schema.columns` SHALL equal the number of detected columns
- **AND** `block.schema.column_widths_pt` SHALL list the width in points of each column
- **AND** `block.schema.tailwind_grid_cols` SHALL reflect column width ratios（如 `"grid-cols-[3fr_1fr_1fr]"`）

#### Scenario: 欄位對齊方式偵測

- **GIVEN** 表格某欄的所有儲存格文字 x0 座標普遍靠近儲存格左邊界
- **WHEN** backend 計算 offset ratio（text x0 相對 cell x0 的比例）
- **THEN** `block.schema.alignments[i]` SHALL be `"text-left"`

- **GIVEN** 表格某欄的所有儲存格文字 x0 座標普遍靠近儲存格右邊界（offset ratio > 0.6）
- **WHEN** backend 計算 offset ratio
- **THEN** `block.schema.alignments[i]` SHALL be `"text-right"`

- **GIVEN** 表格某欄的所有儲存格文字 x0 座標普遍位於儲存格中央（offset ratio 在 0.3–0.6 之間）
- **WHEN** backend 計算 offset ratio
- **THEN** `block.schema.alignments[i]` SHALL be `"text-center"`

#### Scenario: 橫線（border）偵測

- **GIVEN** pdfplumber 在表格 bbox 範圍內偵測到水平線條（`page.lines`）
- **WHEN** backend 分析表格樣式
- **THEN** `block.schema.has_border` SHALL be `true`

- **GIVEN** pdfplumber 在表格 bbox 範圍內未偵測到水平線條
- **WHEN** backend 分析表格樣式
- **THEN** `block.schema.has_border` SHALL be `false`

#### Scenario: 儲存格內距估算

- **GIVEN** 表格儲存格內的字元 y0 與 cell top/bottom 邊界存在空白距離
- **WHEN** backend 計算字元座標與儲存格邊界的距離
- **THEN** `block.schema.cell_padding` SHALL be a Tailwind class string（如 `"py-[8px] px-[6px]"`）reflecting the estimated padding

---

### Requirement: LayoutSpec response schema

Backend SHALL define a `LayoutSpec` Pydantic schema as the response model for `POST /api/pdf/analyze`.

#### Scenario: LayoutSpec 結構完整性

- **GIVEN** backend 成功分析一份 PDF
- **WHEN** backend 回傳 `LayoutSpec`
- **THEN** response SHALL contain `canvas`（包含 `size`、`width_pt`、`height_pt`、`tailwind_page_class`）
- **AND** response SHALL contain `pages`（陣列，每項包含 `page`、`typography_tokens`、`blocks`）
- **AND** each `block` SHALL contain `id`、`type`、`bbox`、`tailwind_layout`
- **AND** blocks with `type: "table"` SHALL additionally contain `schema`
