from dataclasses import dataclass
from typing import TYPE_CHECKING

from src.gym_management.domain.gym.aggregate_root import Gym
from src.shared_kernel.domain.event import DomainEvent

if TYPE_CHECKING:
    from src.gym_management.domain.subscription.aggregate_root import Subscription


@dataclass(kw_only=True)
class GymAddedEvent(DomainEvent):
    subscription: "Subscription"
    gym: Gym


@dataclass
class SomeEvent(DomainEvent):
    pass
