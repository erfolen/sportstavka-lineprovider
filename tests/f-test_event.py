import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.model import EventBD
from datetime import datetime

# Тест для создания объекта Direction
@pytest.mark.asyncio
async def test_create_event(get_async_session: AsyncSession):
    # Создаем новый объект Direction
    new_event = EventBD (
        event_id = "event_247",
        coefficient = "3.5",
        deadline = "2024-09-16T18:57:00",
        state = "new"
    )

    # Добавляем объект в базу данных
    async with get_async_session as session:
        session.add(new_event)
        await session.commit()
        await session.refresh(new_event)

    # Проверяем, что объект был успешно добавлен
    assert new_event.event_id is not None
    assert new_event.coefficient == "3.5"
    assert new_event.deadline == "2024-09-16T18:57:00"
    assert new_event.state == "new"


