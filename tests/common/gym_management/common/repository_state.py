from dataclasses import dataclass, field
from typing import List

from src.gym_management.application.common.dto.repository import AdminDB, GymDB, RoomDB, SubscriptionDB


@dataclass
class RepositorySharedState:
    admins: List[AdminDB] = field(default_factory=list)
    subscriptions: List[SubscriptionDB] = field(default_factory=list)
    gyms: List[GymDB] = field(default_factory=list)
    rooms: List[RoomDB] = field(default_factory=list)
