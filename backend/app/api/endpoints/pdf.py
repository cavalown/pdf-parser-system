from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas.pdf import ParseResponse
from app.services.pdf_service import parse_pdf

router = APIRouter()


@router.post("/parse", response_model=ParseResponse)
async def parse_pdf_endpoint(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF")

    content = await file.read()
    return parse_pdf(filename=file.filename or "unknown.pdf", content=content)
