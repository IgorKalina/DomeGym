import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.gym_management.infrastructure.common.postgres.models.base_model import TimedBaseModel


class Gym(TimedBaseModel):
    __tablename__ = "gym"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    subscription_id: Mapped[uuid.UUID] = mapped_column(primary_key=True)

    def __repr__(self) -> str:
        return f"Gym(id={self.id!r}, name={self.name!r}"
