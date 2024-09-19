import pytest

from app.model import EventBD



@pytest.mark.asyncio
async def test_create_event( prepare_database, client, session):
    """Тест создания события"""
    # Данные для нового события
    event_data = {
        "event_id": "event_247",
        "coefficient": "3.5",
        "deadline": "2024-09-16T18:57:00",
        "state": "new"
    }
    async for cl in client:
    #     # Отправляем запрос на создание события

        response = await cl.post("/event", params=event_data)


            # Проверяем успешный ответ
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["status"] == 201
        assert response_data["detail"] == "Событие создано"

            # Проверяем, что событие действительно записалось в базу данных
        async for session in session:
            event_in_db = await session.get(EventBD, "event_247")
            assert event_in_db is not None
            assert event_in_db.event_id == "event_247"
            assert event_in_db.coefficient == 3.5
            assert event_in_db.deadline.isoformat()  == "2024-09-16T18:57:00"
            assert event_in_db.state.value  == "new"