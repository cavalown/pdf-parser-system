from typing import Literal, Optional

from pydantic import BaseModel, Field


class BBox(BaseModel):
    x0: float = Field(description="Left x coordinate in points")
    top: float = Field(description="Top y coordinate in points (0 = page top)")
    x1: float = Field(description="Right x coordinate in points")
    bottom: float = Field(description="Bottom y coordinate in points")


class TableSchema(BaseModel):
    columns: int = Field(description="Number of columns")
    tailwind_grid_cols: str = Field(description="Tailwind grid-cols class, e.g. grid-cols-[3fr_1fr_1fr]")
    column_widths_pt: list[float] = Field(description="Width of each column in points")
    alignments: list[str] = Field(description="Tailwind text alignment per column, e.g. text-left")
    has_border: bool = Field(description="Whether the table has horizontal border lines")
    cell_padding: str = Field(description="Tailwind padding class for cells, e.g. py-[8px] px-[6px]")


class LayoutBlock(BaseModel):
    id: str = Field(description="Block identifier, e.g. p1_block_0")
    type: Literal["header", "footer", "text", "two_column", "table"] = Field(
        description="Visual block type"
    )
    bbox: BBox = Field(description="Bounding box in PDF points")
    tailwind_layout: str = Field(description="Tailwind layout classes for this block")
    schema_: Optional[TableSchema] = Field(
        default=None, alias="schema", description="Table schema, present only when type is table"
    )

    model_config = {"populate_by_name": True}


class TypographyTokens(BaseModel):
    h1: str = Field(description="Tailwind classes for the largest heading, e.g. text-[24pt] font-bold text-slate-900")
    label: str = Field(description="Tailwind classes for labels/subheadings")
    body: str = Field(description="Tailwind classes for body text (most frequent font size)")


class PageAnalysis(BaseModel):
    page: int = Field(description="Page number, 1-indexed")
    typography_tokens: TypographyTokens
    blocks: list[LayoutBlock] = Field(description="Layout blocks ordered top-to-bottom")


class Canvas(BaseModel):
    size: Literal["A4", "Letter", "Custom"] = Field(description="Page size classification")
    width_pt: float = Field(description="Page width in points")
    height_pt: float = Field(description="Page height in points")
    tailwind_page_class: str = Field(
        description="Tailwind classes for the page shell, e.g. w-[210mm] h-[297mm] p-[20mm] bg-white"
    )


class LayoutSpec(BaseModel):
    canvas: Canvas
    pages: list[PageAnalysis]
