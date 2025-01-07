import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.gym_management.domain.subscription.subscription_type import SubscriptionType
from src.gym_management.infrastructure.common.postgres.models.base_model import TimedBaseModel


class Subscription(TimedBaseModel):
    __tablename__ = "subscription"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    type: Mapped[SubscriptionType] = mapped_column(String(30))
    admin_id: Mapped[uuid.UUID]

    def __repr__(self) -> str:
        return f"Subscription(id={self.id!r}, type={self.type!r}"
