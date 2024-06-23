import uuid
from dataclasses import dataclass

from src.gym_management.domain.common.aggregate_root import AggregateRoot


@dataclass(kw_only=True)
class Room(AggregateRoot):
    name: str
    gym_id: uuid.UUID
    max_daily_sessions: int
