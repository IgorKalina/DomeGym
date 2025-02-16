import uuid
from typing import List, Self

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.gym_management.application.common.dto.repository.subscription import SubscriptionDB
from src.gym_management.domain.subscription import Subscription as SubscriptionAggregate
from src.gym_management.domain.subscription import SubscriptionType
from src.gym_management.infrastructure.common.postgres.models.base_model import BaseModel, TimedBaseModel


class Subscription(TimedBaseModel):
    __tablename__ = "subscription"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    type: Mapped[SubscriptionType] = mapped_column(String(30))
    admin_id: Mapped[uuid.UUID] = mapped_column()

    gym_ids: Mapped[List["SubscriptionGymIds"]] = relationship(
        "SubscriptionGymIds", back_populates="subscription", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Subscription(id={self.id!r}, type={self.type!r}"

    @classmethod
    def from_domain(cls, aggregate: SubscriptionAggregate) -> Self:
        return cls(
            id=aggregate.id,
            type=aggregate.type,
            admin_id=aggregate.admin_id,
            created_at=aggregate.created_at,
            updated_at=aggregate.updated_at,
        )

    def to_domain(self) -> SubscriptionDB:
        return SubscriptionAggregate(
            id=self.id,
            type=self.type,
            admin_id=self.admin_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            gym_ids=[gym.gym_id for gym in self.gym_ids],
        )


class SubscriptionGymIds(BaseModel):
    __tablename__ = "subscription_gym_ids"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    gym_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    subscription_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("subscription.id"), nullable=False)

    # Relationship: A GymRoomIds belongs to one Gym
    subscription: Mapped[Subscription] = relationship("Subscription", back_populates="gym_ids")

    # Ensure room_id is unique per gym
    __table_args__ = (UniqueConstraint("subscription_id", "gym_id", name="uq_subscription_gym"),)

    @classmethod
    def from_domain(cls, aggregate: SubscriptionAggregate) -> List[Self]:
        return [
            cls(
                gym_id=gym_id,
                subscription_id=aggregate.id,
            )
            for gym_id in aggregate.gym_ids
        ]
