import sys
import uuid
from typing import List, Optional

from result import Ok, Result

from src.gym_management.domain.common.aggregate_root import AggregateRoot
from src.gym_management.domain.gym.aggregate_root import Gym
from src.gym_management.domain.subscription.errors import SubscriptionErrors
from src.gym_management.domain.subscription.events.gym_added_event import GymAddedEvent
from src.gym_management.domain.subscription.subscription_type import SubscriptionType


class Subscription(AggregateRoot):
    def __init__(
        self,
        subscription_type: SubscriptionType,
        admin_id: Optional[uuid.UUID],
        gym_ids: Optional[List[uuid.UUID]] = None,
    ) -> None:
        super().__init__()

        self.type = subscription_type
        self.admin_id = admin_id

        self._gym_ids = gym_ids or []

    def add_gym(self, gym: Gym) -> Result:
        if len(self._gym_ids) >= self.max_gyms:
            return SubscriptionErrors.cannot_have_more_rooms_than_subscription_allows()
        self._gym_ids.append(gym.id)
        self._create_domain_event(GymAddedEvent(subscription=self, gym=gym))
        return Ok(None)

    def has_gym(self, gym_id: uuid.UUID) -> bool:
        return gym_id in self._gym_ids

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
