import uuid
from typing import List, Self

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.gym_management.domain.gym.aggregate_root import Gym as GymAggregate
from src.gym_management.infrastructure.common.postgres.models.base_model import BaseModel, TimedBaseModel


class Gym(TimedBaseModel):
    __tablename__ = "gym"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    subscription_id: Mapped[uuid.UUID] = mapped_column()
    max_rooms: Mapped[int] = mapped_column()

    room_ids: Mapped[List["GymRoomIds"]] = relationship(
        "GymRoomIds", back_populates="gym", cascade="all, delete-orphan"
    )
    trainer_ids: Mapped[List["GymTrainerIds"]] = relationship(
        "GymTrainerIds", back_populates="gym", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Gym(id={self.id!r}, name={self.name!r}"

    @classmethod
    def from_domain(cls, aggregate: GymAggregate) -> Self:
        return cls(
            id=aggregate.id,
            name=aggregate.name,
            subscription_id=aggregate.subscription_id,
            max_rooms=aggregate.max_rooms,
            created_at=aggregate.created_at,
            updated_at=aggregate.updated_at,
        )

    def to_domain(self) -> GymAggregate:
        return GymAggregate(
            id=self.id,
            name=self.name,
            subscription_id=self.subscription_id,
            max_rooms=self.max_rooms,
            created_at=self.created_at,
            updated_at=self.updated_at,
            room_ids=[room.room_id for room in self.room_ids],
            trainer_ids=[trainer.trainer_id for trainer in self.trainer_ids],
        )


class GymRoomIds(BaseModel):
    __tablename__ = "gym_room_ids"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    room_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    gym_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("gym.id"), nullable=False)

    # Relationship: A GymRoomIds belongs to one Gym
    gym: Mapped[Gym] = relationship("Gym", back_populates="room_ids")

    # Ensure room_id is unique per gym
    __table_args__ = (UniqueConstraint("room_id", "gym_id", name="uq_room_gym"),)

    @classmethod
    def from_domain(cls, aggregate: GymAggregate) -> List[Self]:
        return [
            cls(
                room_id=room_id,
                gym_id=aggregate.id,
            )
            for room_id in aggregate.room_ids
        ]


class GymTrainerIds(BaseModel):
    __tablename__ = "gym_trainer_ids"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    trainer_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    gym_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("gym.id"), nullable=False)

    # Relationship: A GymRoomIds belongs to one Gym
    gym: Mapped[Gym] = relationship("Gym", back_populates="trainer_ids")

    @classmethod
    def from_domain(cls, aggregate: GymAggregate) -> List[Self]:
        return [
            cls(
                room_id=trainer_id,
                gym_id=aggregate.id,
            )
            for trainer_id in aggregate.trainer_ids
        ]
