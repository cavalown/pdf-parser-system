import io
import math
import statistics
from collections import Counter
from typing import Optional

import pdfplumber

from app.schemas.pdf_analyze import (
    BBox,
    Canvas,
    LayoutBlock,
    LayoutSpec,
    PageAnalysis,
    TableSchema,
    TypographyTokens,
)

_PT_TO_PX = 1.333
_PT_TO_MM = 0.352778

_A4_W = 595.28
_A4_H = 841.89
_LETTER_W = 612.0
_LETTER_H = 792.0
_SIZE_TOLERANCE = 5.0


def _infer_font_weight(fontname: str) -> str:
    lower = fontname.lower()
    if "bold" in lower:
        return "font-bold"
    if "medium" in lower:
        return "font-medium"
    return "font-normal"


def _pt_to_mm_str(pt: float) -> str:
    mm = round(pt * _PT_TO_MM)
    return f"{mm}mm"


def _pt_to_px_str(pt: float) -> str:
    px = round(pt * _PT_TO_PX)
    return f"{px}px"


def _extract_canvas(page: "pdfplumber.page.Page", all_pages: list) -> Canvas:
    w = page.width
    h = page.height

    if abs(w - _A4_W) <= _SIZE_TOLERANCE and abs(h - _A4_H) <= _SIZE_TOLERANCE:
        size = "A4"
        size_class = "w-[210mm] h-[297mm]"
    elif abs(w - _LETTER_W) <= _SIZE_TOLERANCE and abs(h - _LETTER_H) <= _SIZE_TOLERANCE:
        size = "Letter"
        size_class = "w-[216mm] h-[279mm]"
    else:
        size = "Custom"
        size_class = f"w-[{_pt_to_mm_str(w)}] h-[{_pt_to_mm_str(h)}]"

    # Infer margins from median x0 across all pages
    all_x0: list[float] = []
    all_x1: list[float] = []
    all_tops: list[float] = []
    all_bottoms: list[float] = []
    for p in all_pages:
        chars = [c for c in p.chars if c["text"].strip()]
        if chars:
            all_x0.extend(c["x0"] for c in chars)
            all_x1.extend(c["x1"] for c in chars)
            all_tops.extend(c["top"] for c in chars)
            all_bottoms.extend(c["bottom"] for c in chars)

    if all_x0:
        left_margin_pt = statistics.median(all_x0)
        right_margin_pt = w - statistics.median(all_x1)
        top_margin_pt = statistics.median(all_tops)
        bottom_margin_pt = h - statistics.median(all_bottoms)

        lm = round(left_margin_pt * _PT_TO_MM)
        rm = round(right_margin_pt * _PT_TO_MM)
        tm = round(top_margin_pt * _PT_TO_MM)
        bm = round(bottom_margin_pt * _PT_TO_MM)

        if lm == rm == tm == bm:
            padding_class = f"p-[{lm}mm]"
        elif lm == rm and tm == bm:
            padding_class = f"px-[{lm}mm] py-[{tm}mm]"
        else:
            padding_class = f"pt-[{tm}mm] pr-[{rm}mm] pb-[{bm}mm] pl-[{lm}mm]"
    else:
        padding_class = "p-[20mm]"

    tailwind_page_class = f"{size_class} {padding_class} bg-white"
    return Canvas(size=size, width_pt=round(w, 2), height_pt=round(h, 2), tailwind_page_class=tailwind_page_class)


def _extract_typography_tokens(page: "pdfplumber.page.Page") -> TypographyTokens:
    chars = [c for c in page.chars if c["text"].strip() and c.get("size", 0) > 0]

    if not chars:
        return TypographyTokens(
            h1="text-[12pt] font-bold text-slate-900",
            label="text-[11pt] font-semibold text-slate-700",
            body="text-[10pt] font-normal text-slate-600",
        )

    size_counts: Counter = Counter(round(c["size"], 1) for c in chars)
    body_size = size_counts.most_common(1)[0][0]
    all_sizes = sorted(size_counts.keys())
    h1_size = max(all_sizes)

    # Representative char for each level
    h1_chars = [c for c in chars if round(c["size"], 1) == h1_size]
    body_chars = [c for c in chars if round(c["size"], 1) == body_size]

    # label: intermediate size, or bold chars at body size
    label_size = None
    for s in sorted(all_sizes, reverse=True):
        if s < h1_size and s > body_size:
            label_size = s
            break
    if label_size is None:
        bold_body = [c for c in body_chars if "bold" in c.get("fontname", "").lower()]
        label_chars = bold_body if bold_body else body_chars
        label_size = body_size
    else:
        label_chars = [c for c in chars if round(c["size"], 1) == label_size]

    h1_fontname = h1_chars[0].get("fontname", "") if h1_chars else ""
    label_fontname = label_chars[0].get("fontname", "") if label_chars else ""
    body_fontname = body_chars[0].get("fontname", "") if body_chars else ""

    h1_weight = _infer_font_weight(h1_fontname)
    label_weight = _infer_font_weight(label_fontname)
    body_weight = _infer_font_weight(body_fontname)

    return TypographyTokens(
        h1=f"text-[{h1_size}pt] {h1_weight} text-slate-900",
        label=f"text-[{label_size}pt] {label_weight} text-slate-700",
        body=f"text-[{body_size}pt] {body_weight} text-slate-600",
    )


def _words_to_lines(words: list[dict], line_tolerance: float = 3.0) -> list[list[dict]]:
    if not words:
        return []
    sorted_words = sorted(words, key=lambda w: (w["top"], w["x0"]))
    lines: list[list[dict]] = []
    current_line: list[dict] = [sorted_words[0]]
    for w in sorted_words[1:]:
        if abs(w["top"] - current_line[-1]["top"]) <= line_tolerance:
            current_line.append(w)
        else:
            lines.append(current_line)
            current_line = [w]
    lines.append(current_line)
    return lines


def _lines_to_blocks(lines: list[list[dict]], gap_factor: float = 1.5) -> list[list[list[dict]]]:
    if not lines:
        return []
    line_heights = []
    for line in lines:
        heights = [w.get("height", w["bottom"] - w["top"]) for w in line]
        if heights:
            line_heights.append(max(heights))
    avg_line_height = statistics.mean(line_heights) if line_heights else 12.0
    threshold = avg_line_height * gap_factor

    blocks: list[list[list[dict]]] = [[lines[0]]]
    for i in range(1, len(lines)):
        prev_bottom = max(w["bottom"] for w in lines[i - 1])
        curr_top = min(w["top"] for w in lines[i])
        gap = curr_top - prev_bottom
        if gap > threshold:
            blocks.append([lines[i]])
        else:
            blocks[-1].append(lines[i])
    return blocks


def _block_bbox(block_lines: list[list[dict]]) -> BBox:
    all_words = [w for line in block_lines for w in line]
    return BBox(
        x0=min(w["x0"] for w in all_words),
        top=min(w["top"] for w in all_words),
        x1=max(w["x1"] for w in all_words),
        bottom=max(w["bottom"] for w in all_words),
    )


def _bbox_overlap(b1: BBox, b2_x0: float, b2_top: float, b2_x1: float, b2_bottom: float) -> bool:
    return not (b1.x1 <= b2_x0 or b2_x1 <= b1.x0 or b1.bottom <= b2_top or b2_bottom <= b1.top)


def _extract_table_schema(table, page: "pdfplumber.page.Page") -> TableSchema:
    bbox = table.bbox  # (x0, top, x1, bottom)
    col_positions = table.col_positions  # sorted list of x boundaries

    n_cols = len(col_positions) - 1
    col_widths = [round(col_positions[i + 1] - col_positions[i], 2) for i in range(n_cols)]

    # fr ratios: divide by min width then simplify with GCD
    min_w = min(col_widths) if col_widths else 1.0
    raw_frs = [max(1, round(w / min_w)) for w in col_widths]
    g = raw_frs[0]
    for v in raw_frs[1:]:
        g = math.gcd(g, v)
    frs = [v // g for v in raw_frs]
    # cap individual fr values to avoid absurdly large numbers
    if max(frs) > 12:
        total = sum(frs)
        frs = [max(1, round(v / total * 12)) for v in frs]
    grid_cols = "grid-cols-[" + "_".join(f"{v}fr" for v in frs) + "]"

    # Alignment per column
    all_chars = [c for c in page.chars if c["text"].strip()]
    alignments: list[str] = []
    for i in range(n_cols):
        cx0 = col_positions[i]
        cx1 = col_positions[i + 1]
        cell_width = cx1 - cx0
        if cell_width <= 0:
            alignments.append("text-left")
            continue
        col_chars = [
            c for c in all_chars
            if cx0 <= c["x0"] < cx1 and bbox[1] <= c["top"] < bbox[3]
        ]
        if not col_chars:
            alignments.append("text-left")
            continue
        offsets = [(c["x0"] - cx0) / cell_width for c in col_chars]
        median_offset = statistics.median(offsets)
        if median_offset < 0.3:
            alignments.append("text-left")
        elif median_offset > 0.6:
            alignments.append("text-right")
        else:
            alignments.append("text-center")

    # Border detection
    table_lines = [
        ln for ln in page.lines
        if bbox[0] <= ln["x0"] and ln["x1"] <= bbox[2]
        and bbox[1] <= ln["top"] and ln["bottom"] <= bbox[3]
        and abs(ln["top"] - ln["bottom"]) < 2  # horizontal line
    ]
    has_border = len(table_lines) > 0

    # Cell padding: estimate from first data row chars
    padding_pt = 4.0
    if len(table.rows) > 0:
        row = table.rows[0]
        cell_tops = [c[1] for c in row if c]
        cell_bottoms = [c[3] for c in row if c]
        if cell_tops and cell_bottoms:
            cell_top = min(cell_tops)
            cell_bottom = max(cell_bottoms)
            row_chars = [
                c for c in all_chars
                if cell_top <= c["top"] < cell_bottom
            ]
            if row_chars:
                avg_char_top = statistics.mean(c["top"] for c in row_chars)
                avg_char_bottom = statistics.mean(c["bottom"] for c in row_chars)
                padding_pt = max(2.0, (avg_char_top - cell_top + cell_bottom - avg_char_bottom) / 2)
    padding_px = round(padding_pt * _PT_TO_PX)
    cell_padding = f"py-[{padding_px}px] px-[{max(4, padding_px - 2)}px]"

    return TableSchema(
        columns=n_cols,
        tailwind_grid_cols=grid_cols,
        column_widths_pt=col_widths,
        alignments=alignments,
        has_border=has_border,
        cell_padding=cell_padding,
    )


def _extract_blocks(
    page: "pdfplumber.page.Page",
    page_idx: int,
    tables: list,
) -> list[LayoutBlock]:
    words = page.extract_words(extra_attrs=["fontname", "size"])
    if not words:
        return []

    lines = _words_to_lines(words)
    block_line_groups = _lines_to_blocks(lines)
    page_width = page.width
    blocks: list[LayoutBlock] = []

    for block_idx, block_lines in enumerate(block_line_groups):
        bbox = _block_bbox(block_lines)
        block_id = f"p{page_idx + 1}_block_{block_idx}"

        # Check table overlap
        matched_table = None
        for tbl in tables:
            tb = tbl.bbox  # (x0, top, x1, bottom)
            if _bbox_overlap(bbox, tb[0], tb[1], tb[2], tb[3]):
                matched_table = tbl
                break

        if matched_table is not None:
            table_schema = _extract_table_schema(matched_table, page)
            blocks.append(
                LayoutBlock(
                    id=block_id,
                    type="table",
                    bbox=bbox,
                    tailwind_layout="w-full",
                    **{"schema": table_schema},
                )
            )
            continue

        # Non-table: detect layout direction
        all_block_words = [w for line in block_lines for w in line]
        x0_values = sorted(w["x0"] for w in all_block_words)

        # Look for horizontal gap > 10% page width
        gap_threshold = page_width * 0.10
        split_x: Optional[float] = None
        for i in range(len(x0_values) - 1):
            gap = x0_values[i + 1] - x0_values[i]
            if gap > gap_threshold:
                split_x = (x0_values[i] + x0_values[i + 1]) / 2
                break

        if split_x is not None:
            left_words = [w for w in all_block_words if w["x0"] < split_x]
            right_words = [w for w in all_block_words if w["x0"] >= split_x]
            left_width = (split_x - bbox.x0) if left_words else 1
            right_width = (bbox.x1 - split_x) if right_words else 1
            total_w = left_width + right_width
            left_fr = max(1, round(left_width / total_w * 12))
            right_fr = max(1, round(right_width / total_w * 12))
            g = math.gcd(left_fr, right_fr)
            left_fr //= g
            right_fr //= g
            gap_px = round((split_x - max(w["x1"] for w in left_words)) * _PT_TO_PX) if left_words else 16
            gap_px = max(8, gap_px)
            tailwind_layout = f"grid grid-cols-[{left_fr}fr_{right_fr}fr] gap-[{gap_px}px]"
            block_type = "two_column"
        else:
            # Compute average vertical spacing between lines
            line_tops = [min(w["top"] for w in line) for line in block_lines]
            if len(line_tops) > 1:
                spacings = [line_tops[i + 1] - line_tops[i] for i in range(len(line_tops) - 1)]
                avg_spacing_px = round(statistics.mean(spacings) * _PT_TO_PX)
            else:
                avg_spacing_px = 8
            avg_spacing_px = max(4, avg_spacing_px)
            tailwind_layout = f"flex flex-col space-y-[{avg_spacing_px}px]"
            block_type = "text"

        blocks.append(
            LayoutBlock(
                id=block_id,
                type=block_type,
                bbox=bbox,
                tailwind_layout=tailwind_layout,
            )
        )

    # Sort top-to-bottom
    blocks.sort(key=lambda b: b.bbox.top)
    return blocks


def _classify_header_footer_single_page(
    blocks: list[LayoutBlock], page_height: float
) -> list[LayoutBlock]:
    for block in blocks:
        if block.type in ("header", "footer"):
            continue
        if block.bbox.top < page_height * 0.15:
            block.type = "header"
        elif block.bbox.bottom > page_height * 0.90:
            block.type = "footer"
    return blocks


def _detect_header_footer_multi_page(
    pages_blocks: list[list[LayoutBlock]], page_height: float
) -> list[list[LayoutBlock]]:
    n_pages = len(pages_blocks)
    if n_pages < 2:
        return pages_blocks

    # Collect normalized y-center per block per page
    # group_key → list of (page_idx, block_idx)
    def norm_y_center(block: LayoutBlock) -> float:
        return (block.bbox.top + block.bbox.bottom) / 2 / page_height

    # Build position groups across pages
    groups: list[dict] = []  # {norm_y, page_idxs: set, block_refs: list[(page_idx, blk_idx)]}
    for page_idx, blocks in enumerate(pages_blocks):
        for blk_idx, block in enumerate(blocks):
            if block.type in ("header", "footer"):
                continue
            ny = norm_y_center(block)
            matched = None
            for grp in groups:
                if abs(grp["norm_y"] - ny) <= 0.05:
                    matched = grp
                    break
            if matched:
                matched["page_idxs"].add(page_idx)
                matched["block_refs"].append((page_idx, blk_idx))
                # Update running average
                matched["norm_y"] = (matched["norm_y"] + ny) / 2
            else:
                groups.append({
                    "norm_y": ny,
                    "page_idxs": {page_idx},
                    "block_refs": [(page_idx, blk_idx)],
                })

    for grp in groups:
        if len(grp["page_idxs"]) / n_pages <= 0.5:
            continue
        ny = grp["norm_y"]
        if ny < 0.15:
            new_type = "header"
        elif ny > 0.90:
            new_type = "footer"
        else:
            continue
        for page_idx, blk_idx in grp["block_refs"]:
            pages_blocks[page_idx][blk_idx].type = new_type

    return pages_blocks


def analyze_pdf(content: bytes) -> LayoutSpec:
    with pdfplumber.open(io.BytesIO(content)) as pdf:
        all_pages = pdf.pages
        canvas = _extract_canvas(all_pages[0], all_pages)

        pages_blocks: list[list[LayoutBlock]] = []
        pages_typography: list[TypographyTokens] = []

        for page_idx, page in enumerate(all_pages):
            tables = page.find_tables()
            typography = _extract_typography_tokens(page)
            blocks = _extract_blocks(page, page_idx, tables)
            pages_blocks.append(blocks)
            pages_typography.append(typography)

        page_height = all_pages[0].height
        if len(all_pages) == 1:
            pages_blocks[0] = _classify_header_footer_single_page(pages_blocks[0], page_height)
        else:
            pages_blocks = _detect_header_footer_multi_page(pages_blocks, page_height)

        page_analyses = [
            PageAnalysis(
                page=idx + 1,
                typography_tokens=pages_typography[idx],
                blocks=pages_blocks[idx],
            )
            for idx in range(len(all_pages))
        ]

    return LayoutSpec(canvas=canvas, pages=page_analyses)
