import uuid

from src.shared_kernel.domain.common.aggregate_root import AggregateRoot


class Room(AggregateRoot):
    name: str
    gym_id: uuid.UUID
    max_daily_sessions: int
