import sys
import uuid
from typing import Any, Dict, List

from src.gym_management.domain.common.aggregate_root import AggregateRoot
from src.gym_management.domain.gym.aggregate_root import Gym
from src.gym_management.domain.subscription.errors import SubscriptionCannotHaveMoreGymsThanSubscriptionAllows
from src.gym_management.domain.subscription.events.gym_added_event import GymAddedEvent
from src.gym_management.domain.subscription.subscription_type import SubscriptionType
from src.shared_kernel.error_or import ErrorOr, ErrorResult, OkResult


class Subscription(AggregateRoot):
    def __init__(
        self,
        subscription_type: SubscriptionType,
        admin_id: uuid.UUID,
        id: uuid.UUID | None = None,
        gym_ids: List[uuid.UUID] | None = None,
    ) -> None:
        super_kwargs: Dict[str, Any] = {}
        if id is not None:
            super_kwargs["id"] = id
        super().__init__(**super_kwargs)

        self.type = subscription_type
        self.admin_id = admin_id

        self._gym_ids: List[uuid.UUID] = gym_ids or []

    def add_gym(self, gym: Gym) -> ErrorOr[Gym]:
        if len(self._gym_ids) >= self.max_gyms:
            return ErrorResult(SubscriptionCannotHaveMoreGymsThanSubscriptionAllows())
        self._gym_ids.append(gym.id)
        self._create_domain_event(GymAddedEvent(subscription=self, gym=gym))
        return OkResult(gym)

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
