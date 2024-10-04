import decimal
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from app.model import StatusEvent

class SEvent(BaseModel):
    event_id: Optional[str] = None
    coefficient: decimal.Decimal = Field(ge=0)
    deadline: datetime
    state: StatusEvent

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "event_id": "abc123",
                "coefficient": "1.25",
                "deadline": "2024-12-31T23:59:59",
                "state": "active"
            }
        }
    )

class SEventState(BaseModel):
    event_id: str
    state: StatusEvent
