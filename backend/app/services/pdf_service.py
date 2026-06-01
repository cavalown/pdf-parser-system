import io
from pypdf import PdfReader

from app.schemas.pdf import PageResult, ParseResponse


def parse_pdf(filename: str, content: bytes) -> ParseResponse:
    reader = PdfReader(io.BytesIO(content))
    pages = [
        PageResult(page=i + 1, text=page.extract_text() or "")
        for i, page in enumerate(reader.pages)
    ]
    return ParseResponse(filename=filename, total_pages=len(pages), pages=pages)
