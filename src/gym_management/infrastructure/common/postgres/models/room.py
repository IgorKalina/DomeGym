import uuid
from typing import Self

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.gym_management.application.common.dto.repository.gym import GymDB
from src.gym_management.application.common.dto.repository.room import RoomDB
from src.gym_management.infrastructure.common.postgres.models.base_model import TimedBaseModel


class Room(TimedBaseModel):
    __tablename__ = "room"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    gym_id: Mapped[uuid.UUID] = mapped_column()
    subscription_id: Mapped[uuid.UUID] = mapped_column()

    def __repr__(self) -> str:
        return (
            f"Room(id={self.id!r}, name={self.name!r}, gym_id={self.gym_id!r}, subscription_id={self.subscription_id!r}"
        )

    @classmethod
    def from_dto(cls, dto: RoomDB) -> Self:
        return cls(
            id=dto.id,
            name=dto.name,
            gym_id=dto.gym_id,
            subscription_id=dto.subscription_id,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )

    def to_dto(self) -> GymDB:
        return RoomDB(
            id=self.id,
            name=self.name,
            gym_id=self.gym_id,
            subscription_id=self.subscription_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
