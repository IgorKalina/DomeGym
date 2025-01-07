import uuid

from sqlalchemy.orm import Mapped, mapped_column

from src.gym_management.infrastructure.common.postgres.models.base_model import TimedBaseModel


class Admin(TimedBaseModel):
    __tablename__ = "admin"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column()

    def __repr__(self) -> str:
        return f"Admin(id={self.id!r}, user_id={self.user_id!r}"
