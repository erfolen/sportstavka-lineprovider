from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import SEvent, SEventState
from app.service import EventDal
from app.database import get_async_session

router = APIRouter(
    prefix='',
    tags=['Events']
)


@router.post('/event')
async def create_event(
        event: Annotated[SEvent, Depends()], session: AsyncSession =
        Depends(get_async_session),
) -> dict:
    """Создание события, если id уже есть то возвращается событие."""
    if await EventDal.check_event_id(event.event_id, session):
        event_db = await EventDal.get_event(event.event_id, session)
        event_s = SEvent.model_validate(event_db)
        return {"status": 200, "detail": "Событие уже есть",
                **event_s.model_dump()}
    event_id = await EventDal.create_event(event, session)
    event.event_id = event_id
    return {"status": 201, "detail": "Событие создано", **event.model_dump()}


@router.get('/event')
async def get_event(event_id: str, session: AsyncSession = Depends(
    get_async_session)) -> dict:
    """Получение события по ид."""
    if await EventDal.check_event_id(event_id, session):
        event_db = await EventDal.get_event(event_id, session)
        event_s = SEvent.model_validate(event_db)
        return {"status": 200, **event_s.model_dump()}
    else:
        return {"status": 404, "detail": f"Событие c id={event_id} не найдено"}


@router.get('/events')
async def get_events(session: AsyncSession = Depends(get_async_session)) -> (
        list):
    """Получение всех событий"""
    return await EventDal.find_all_events(session)


@router.patch('/event')
async def change_state(event_state: Annotated[SEventState, Depends()], session:
AsyncSession =
Depends(get_async_session)) -> dict:
    """Обновление состояния события по id"""
    event = await EventDal.change_state(event_state, session)
    if event is not None:
        return {"status": 200, "detail": "Статус был обновлен",
                **event.model_dump()}
    else:
        return {"status": 404,
                "detail": f"Событие c id={event_state.event_id} не "
                          f"найдено"}
