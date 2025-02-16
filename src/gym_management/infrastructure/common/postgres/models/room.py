import uuid
from typing import Self

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.gym_management.domain.room.aggregate_root import Room as RoomAggregate
from src.gym_management.infrastructure.common.postgres.models.base_model import TimedBaseModel


class Room(TimedBaseModel):
    __tablename__ = "room"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    gym_id: Mapped[uuid.UUID] = mapped_column()
    max_daily_sessions: Mapped[int] = mapped_column()

    def __repr__(self) -> str:
        return (
            f"Room(id={self.id!r}, name={self.name!r}, gym_id={self.gym_id!r}, subscription_id={self.subscription_id!r}"
        )

    @classmethod
    def from_domain(cls, aggregate: RoomAggregate) -> Self:
        return cls(
            id=aggregate.id,
            name=aggregate.name,
            gym_id=aggregate.gym_id,
            max_daily_sessions=aggregate.max_daily_sessions,
            created_at=aggregate.created_at,
            updated_at=aggregate.updated_at,
        )

    def to_domain(self) -> RoomAggregate:
        return RoomAggregate(
            id=self.id,
            name=self.name,
            gym_id=self.gym_id,
            max_daily_sessions=self.max_daily_sessions,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
