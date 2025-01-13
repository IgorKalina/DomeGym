import sys
import uuid
from copy import copy
from typing import List

from src.gym_management.domain.common.aggregate_root import AggregateRoot
from src.gym_management.domain.gym.aggregate_root import Gym
from src.gym_management.domain.subscription.events.gym_added_event import GymAddedEvent
from src.gym_management.domain.subscription.exceptions import SubscriptionCannotHaveMoreGymsThanSubscriptionAllowsError
from src.gym_management.domain.subscription.subscription_type import SubscriptionType


class Subscription(AggregateRoot):
    def __init__(
        self,
        *args,
        type: SubscriptionType,
        admin_id: uuid.UUID,
        gym_ids: List[uuid.UUID] | None = None,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self.type = type
        self.admin_id = admin_id

        self.__gym_ids = gym_ids or []

    def add_gym(self, gym: Gym) -> None:
        if len(self.__gym_ids) >= self.max_gyms:
            raise SubscriptionCannotHaveMoreGymsThanSubscriptionAllowsError(max_gyms=self.max_gyms)
        self.__gym_ids.append(gym.id)
        self._create_domain_event(GymAddedEvent(subscription=self, gym=gym))

    def has_gym(self, gym_id: uuid.UUID) -> bool:
        return gym_id in self.__gym_ids

    @property
    def gym_ids(self) -> List[uuid.UUID]:
        return copy(self.__gym_ids)

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
