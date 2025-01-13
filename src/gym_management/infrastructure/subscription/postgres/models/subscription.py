import uuid
from typing import List, Self

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.gym_management.application.subscription.dto.repository import SubscriptionDB
from src.gym_management.domain.subscription.subscription_type import SubscriptionType
from src.gym_management.infrastructure.common.postgres.models.base_model import TimedBaseModel


class Subscription(TimedBaseModel):
    __tablename__ = "subscription"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    type: Mapped[SubscriptionType] = mapped_column(String(30))
    admin_id: Mapped[uuid.UUID] = mapped_column()

    def __repr__(self) -> str:
        return f"Subscription(id={self.id!r}, type={self.type!r}"

    @classmethod
    def from_dto(cls, dto: SubscriptionDB) -> Self:
        return cls(
            id=dto.id,
            type=dto.type,
            admin_id=dto.admin_id,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )

    def to_dto(self, gym_ids: List[uuid.UUID] | None = None) -> SubscriptionDB:
        return SubscriptionDB(
            id=self.id,
            type=self.type,
            admin_id=self.admin_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            gym_ids=gym_ids or [],
        )
