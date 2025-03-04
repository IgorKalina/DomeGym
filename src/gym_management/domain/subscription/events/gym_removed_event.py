from typing import TYPE_CHECKING

from src.gym_management.domain.gym.aggregate_root import Gym
from src.shared_kernel.domain.common.event import DomainEvent

if TYPE_CHECKING:
    from src.gym_management.domain.gym.aggregate_root import Gym
    from src.gym_management.domain.subscription.aggregate_root import Subscription


class GymRemovedEvent(DomainEvent):
    subscription: "Subscription"
    gym: "Gym"
