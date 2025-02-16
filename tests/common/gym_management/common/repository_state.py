from dataclasses import dataclass, field
from typing import List

from src.gym_management.application.common.dto.repository import AdminDB
from src.gym_management.domain.gym.aggregate_root import Gym
from src.gym_management.domain.room.aggregate_root import Room
from src.gym_management.domain.subscription.aggregate_root import Subscription


@dataclass
class RepositorySharedState:
    admins: List[AdminDB] = field(default_factory=list)
    subscriptions: List[Subscription] = field(default_factory=list)
    gyms: List[Gym] = field(default_factory=list)
    rooms: List[Room] = field(default_factory=list)
