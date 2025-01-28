import typing

from src.shared_kernel.domain.common.event import DomainEvent

if typing.TYPE_CHECKING:
    from src.gym_management.domain.subscription.aggregate_root import Subscription


class SubscriptionUnsetEvent(DomainEvent):
    subscription: "Subscription"
