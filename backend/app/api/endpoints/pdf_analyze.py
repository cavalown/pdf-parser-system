import json
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas.pdf_analyze import LayoutSpec
from app.services.pdf_analyzer_service import analyze_pdf

router = APIRouter()

_OUTPUT_DIR = Path(__file__).resolve().parents[3] / "output"


@router.post(
    "/analyze",
    response_model=LayoutSpec,
    summary="Analyze PDF layout",
    description=(
        "Upload a computer-generated PDF and receive a Tailwind layout specification JSON, "
        "including canvas dimensions, per-page typography tokens, layout blocks "
        "(header, footer, text, two-column, table), and embedded table schemas. "
        "The result is also saved to backend/output/<filename>_layout.json."
    ),
)
async def analyze_pdf_endpoint(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF")

    content = await file.read()
    result = analyze_pdf(content=content)

    _OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    stem = Path(file.filename or "unknown").stem
    output_path = _OUTPUT_DIR / f"{stem}_layout.json"
    output_path.write_text(
        result.model_dump_json(indent=2, by_alias=True),
        encoding="utf-8",
    )

    return result
