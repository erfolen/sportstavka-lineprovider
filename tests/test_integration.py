import pytest

from app.model import EventBD


@pytest.mark.asyncio
async def test_create_event(ac, db_session):
    """Тест создания события"""
    # Данные для нового события
    event_data = {
        "event_id": "event_230",
        "coefficient": "3.5",
        "deadline": "2024-09-16T18:57:00",
        "state": "new"
    }
    async for client in ac:
        # Отправляем запрос на создание события

        response = await client.post("/event", params=event_data)


        # Проверяем успешный ответ
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["status"] == 200
        assert response_data["data"] == "Событие уже есть"

        # Проверяем, что событие действительно записалось в базу данных
        async for session in db_session:
            event_in_db = await session.get(EventBD, "event_230")
            assert event_in_db is not None
            assert event_in_db.event_id == "event_230"
            assert event_in_db.coefficient == 3.5
            assert event_in_db.deadline  == "2024-09-16T18:57:00"
            assert event_in_db.state  == "new"
