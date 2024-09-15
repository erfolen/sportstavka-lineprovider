import enum
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Numeric, CheckConstraint, TIMESTAMP

from app.database import Base


class StatusEvent(enum.Enum):
    NEW = 'new'
    FINISHED_WIN = 'finished_win'
    FINISHED_LOSE = 'finished_lose'


class Event(Base):
    """События ставок."""
    __tablename__ = 'event'

    event_id: Mapped[str] = mapped_column(primary_key=True)
    coefficient: Mapped[float] = mapped_column(
        Numeric(precision=7, scale=2),  # 7 цифр всего, 2 после запятой
        nullable=False)
    deadline: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False
    )
    state: Mapped[StatusEvent]

    __table_args__ = (
        CheckConstraint('coefficient > 0', name='positive_number'),
    )