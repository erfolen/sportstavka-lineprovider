from app.model import EventBD
from app.schemas import SEvent
from app.database import async_session_fabric


class EventDal:
    @classmethod
    async def create_event(cls, data: SEvent) -> int:
        async with async_session_fabric as session:
            event_dict = data.model_dump()

            event = EventBD(**event_dict)
            session.add(event)
            await  session.flush()
            await session.commit()
            return event.event_id
