from dataclasses import dataclass
from typing import TYPE_CHECKING

from src.gym_management.domain.common.event import DomainEvent

if TYPE_CHECKING:
    from src.gym_management.domain.subscription.aggregate_root import Subscription


@dataclass
class SubscriptionSetEvent(DomainEvent):
    subscription: "Subscription"
