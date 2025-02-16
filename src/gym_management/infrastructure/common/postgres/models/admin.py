import uuid
from typing import Self

from sqlalchemy.orm import Mapped, mapped_column

from src.gym_management.domain.admin.aggregate_root import Admin as AdminAggregate
from src.gym_management.infrastructure.common.postgres.models.base_model import TimedBaseModel


class Admin(TimedBaseModel):
    __tablename__ = "admin"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column()
    subscription_id: Mapped[uuid.UUID] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f"Admin(id={self.id!r}, user_id={self.user_id!r}"

    @classmethod
    def from_domain(cls, aggregate: AdminAggregate) -> Self:
        return cls(
            id=aggregate.id,
            user_id=aggregate.user_id,
            subscription_id=aggregate.subscription_id,
            created_at=aggregate.created_at,
            updated_at=aggregate.updated_at,
        )

    def to_domain(self) -> AdminAggregate:
        return AdminAggregate(
            id=self.id,
            user_id=self.user_id,
            subscription_id=self.subscription_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
