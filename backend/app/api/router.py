from fastapi import APIRouter

from app.api.endpoints import health, pdf, pdf_analyze

router = APIRouter()

router.include_router(health.router)
router.include_router(pdf.router, prefix="/pdf")
router.include_router(pdf_analyze.router, prefix="/pdf")
