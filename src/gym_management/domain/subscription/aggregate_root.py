import sys
import uuid
from dataclasses import dataclass, field
from typing import List

from src.gym_management.domain.common.aggregate_root import AggregateRoot
from src.gym_management.domain.gym.aggregate_root import Gym
from src.gym_management.domain.subscription.events.gym_added_event import GymAddedEvent
from src.gym_management.domain.subscription.subscription_type import SubscriptionType


@dataclass(kw_only=True)
class Subscription(AggregateRoot):
    type: SubscriptionType

    _gym_ids: List[uuid.UUID] = field(default_factory=list)
    _admin_id: uuid.UUID

    @property
    def max_gyms(self) -> int:
        match self.type:
            case SubscriptionType.FREE:
                return 1
            case SubscriptionType.STARTER:
                return 1
            case SubscriptionType.PRO:
                return 3
            case _:
                raise ValueError(f"Unknown subscription type: {self.type}")

    @property
    def max_rooms(self) -> int:
        match self.type:
            case SubscriptionType.FREE:
                return 1
            case SubscriptionType.STARTER:
                return 3
            case SubscriptionType.PRO:
                return sys.maxsize
            case _:
                raise ValueError(f"Unknown subscription type: {self.type}")

    @property
    def max_daily_sessions(self) -> int:
        match self.type:
            case SubscriptionType.FREE:
                return 4
            case SubscriptionType.STARTER:
                return sys.maxsize
            case SubscriptionType.PRO:
                return sys.maxsize
            case _:
                raise ValueError(f"Unknown subscription type: {self.type}")

    def add_gym(self, gym: Gym) -> None:
        if len(self._gym_ids) >= self.max_gyms:
            # todo add error
            return None

        self._gym_ids.append(gym.id)
        self._create_domain_event(GymAddedEvent(subscription=self, gym=gym))

    def has_gym(self, gym_id: uuid.UUID) -> bool:
        return gym_id in self._gym_ids