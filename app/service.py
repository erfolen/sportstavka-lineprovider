import uuid

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.model import EventBD
from app.schemas import SEvent, SEventState
from app.database import async_session_fabric


class EventDal:
    @classmethod
    async def create_event(cls, data: SEvent, session: AsyncSession) -> str:
        """Создание события."""
        event = EventBD(**data.model_dump())

        if event.event_id is None:
            event.event_id = str(uuid.uuid4())

        session.add(event)
        await  session.flush()
        await session.commit()
        return data.event_id

    @classmethod
    async def check_event_id(cls, event_id: str,
                             session: AsyncSession) -> bool:
        """Проверка есть в БД события."""
        query = select(EventBD).where(EventBD.event_id == event_id)
        result = await session.execute(query)
        return result.scalars().first() is not None

    @classmethod
    async def get_event(cls, event_id: str, session: AsyncSession) -> EventBD:
        """Получение события по id."""
        query = select(EventBD).where(EventBD.event_id == event_id)
        event = await session.execute(query)
        return event.scalars().first()

    @classmethod
    async def find_all_events(cls, session: AsyncSession) -> list[SEvent]:
        """Выводит все события."""
        query = select(EventBD)
        result = await session.execute(query)
        events_bd = result.scalars().all()
        return [SEvent.model_validate(event_bd, from_attributes=True) for
                event_bd in events_bd]

    @classmethod
    async def change_state(cls, data: SEventState,
                           session: AsyncSession) -> SEvent | None:
        """Изменения события."""
        event_id, new_state = data.model_dump().values()
        if await cls.check_event_id(event_id, session):
            await session.execute(
                update(EventBD)
                .where(EventBD.event_id == event_id)
                .values(state=new_state)
            )
            await session.commit()

            query = select(EventBD).where(EventBD.event_id == event_id)
            result = await session.execute(query)
            return SEvent.model_validate(result.scalars().first(),
                                         from_attributes=True)
        else:
            return None
