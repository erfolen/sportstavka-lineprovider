from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.sql.annotation import Annotated

from schemas import SEvent
from service import EventDal

router = APIRouter(
    prefix='/event',
    tags=['Events']

)


@router.post('')
async def create_event(
        event: Annotated[SEvent, Depends()],
) -> SEvent:
    event_id = await EventDal.create_event(event)
    return {"status": 200, "data": "Событие создано", "event_id": event_id}

#
# @router.get('{event_id}')
# async def get_event(event_id: str = Path(default=None)):
#     if event_id in events:
#         return events[event_id]
#
#     raise HTTPException(status_code=404, detail="Event not found")
#
#
# @router.get('')
# async def get_events():
#     return list(e for e in events.values() if time.time() < e.deadline)
