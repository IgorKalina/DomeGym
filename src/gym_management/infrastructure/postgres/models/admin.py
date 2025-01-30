import uuid
from typing import Self

from sqlalchemy.orm import Mapped, mapped_column

from src.gym_management.application.common.dto.repository.admin import AdminDB
from src.gym_management.infrastructure.postgres.models.base_model import TimedBaseModel


class Admin(TimedBaseModel):
    __tablename__ = "admin"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column()
    subscription_id: Mapped[uuid.UUID] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f"Admin(id={self.id!r}, user_id={self.user_id!r}"

    @classmethod
    def from_dto(cls, dto: AdminDB) -> Self:
        return cls(
            id=dto.id,
            user_id=dto.user_id,
            subscription_id=dto.subscription_id,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )

    def to_dto(self) -> AdminDB:
        return AdminDB(
            id=self.id,
            user_id=self.user_id,
            subscription_id=self.subscription_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
