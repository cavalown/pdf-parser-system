from datetime import datetime, timezone
from fastapi import APIRouter

from app.schemas.health import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(
        alive=True,
        status="ok",
        service="pdf-parser-system-api",
        checkedAt=datetime.now(timezone.utc),
    )
