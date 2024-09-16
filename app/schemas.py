import decimal
from datetime import datetime
from pydantic import BaseModel, Field

from model import StatusEvent

class SEvent(BaseModel):
    event_id: str
    coefficient: decimal.Decimal = Field(ge=0)
    deadline: datetime
    state: StatusEvent

# class SevenResponse(SEvent):
#     status: 200
#     data: "Событие создано"