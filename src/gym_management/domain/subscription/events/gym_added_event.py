from dataclasses import dataclass
from typing import TYPE_CHECKING

from src.gym_management.domain.common.event import DomainEvent
from src.gym_management.domain.gym.aggregate_root import Gym

if TYPE_CHECKING:
    from src.gym_management.domain.subscription.aggregate_root import Subscription


@dataclass
class GymAddedEvent(DomainEvent):
    subscription: "Subscription"
    gym: Gym
