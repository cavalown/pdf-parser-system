from fastapi import APIRouter, File, HTTPException, UploadFile
from pypdf import PdfReader
import io

router = APIRouter()


@router.post("/parse")
async def parse_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF")

    content = await file.read()
    reader = PdfReader(io.BytesIO(content))

    pages = []
    for i, page in enumerate(reader.pages):
        pages.append({"page": i + 1, "text": page.extract_text() or ""})

    return {
        "filename": file.filename,
        "total_pages": len(reader.pages),
        "pages": pages,
    }
