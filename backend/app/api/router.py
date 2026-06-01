from fastapi import APIRouter

from app.api.endpoints import health, pdf

router = APIRouter()

router.include_router(health.router)
router.include_router(pdf.router, prefix="/pdf")
