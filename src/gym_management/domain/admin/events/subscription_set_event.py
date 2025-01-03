import typing
from dataclasses import dataclass

from src.shared_kernel.domain.event import DomainEvent

if typing.TYPE_CHECKING:
    from src.gym_management.domain.subscription.aggregate_root import Subscription


@dataclass
class SubscriptionSetEvent(DomainEvent):
    subscription: "Subscription"
