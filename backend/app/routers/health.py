from datetime import datetime, timezone
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "alive": True,
        "status": "ok",
        "service": "pdf-parser-system-api",
        "checkedAt": datetime.now(timezone.utc).isoformat(),
    }
