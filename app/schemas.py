import decimal
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.model import StatusEvent

class SEvent(BaseModel):
    event_id: Optional[str] = None
    coefficient: decimal.Decimal = Field(ge=0)
    deadline: datetime
    state: StatusEvent

    class Config:
        from_attributes = True

class SEventState(BaseModel):
    event_id: str
    state: StatusEvent
