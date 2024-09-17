from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends

from app.model import EventBD
from app.schemas import SEvent, SEventState
from app.service import EventDal

router = APIRouter(
    prefix='',
    tags=['Events']
)


@router.post('/event')
async def create_event(
        event: Annotated[SEvent, Depends()],
) -> dict:
    """Создание события, если id уже есть то возвращается событие."""
    if await EventDal.check_event_id(event.event_id):
        event_db = await EventDal.get_event(event.event_id)
        event_s = SEvent.model_validate(event_db)
        return {"status": 200, "data": "Событие уже есть",
                **event_s.model_dump()}
    event_id = await EventDal.create_event(event)
    event.event_id = event_id
    return {"status": 201, "data": "Событие создано", **event.model_dump()}


@router.get('/event')
async def get_event(event_id: str) -> dict:
    """Получение события по ид."""
    if await EventDal.check_event_id(event_id):
        event_db = await EventDal.get_event(event_id)
        event_s = SEvent.model_validate(event_db)
        return {"status": 200, **event_s.model_dump()}
    else:
        return {"status": 404, "data": f"Событие c id={event_id} не найдено"}


@router.get('/events')
async def get_events():
    """Получение всех событий"""
    return await EventDal.find_all_events()


@router.patch('/event')
async def change_state(event_state: Annotated[SEventState, Depends()]) -> dict:
    """Обновление состояния события по id"""
    event = await EventDal.change_state(event_state)
    if event is not None:
        return {"status": 200, "data": "Статус был обновлен",
                **event.model_dump()}
    else:
        return {"status": 404,
                "data": f"Событие c id={event_state.event_id} не "
                        f"найдено"}
