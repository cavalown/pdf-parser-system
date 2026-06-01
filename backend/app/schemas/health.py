from datetime import datetime
from pydantic import BaseModel


class HealthResponse(BaseModel):
    alive: bool
    status: str
    service: str
    checkedAt: datetime
