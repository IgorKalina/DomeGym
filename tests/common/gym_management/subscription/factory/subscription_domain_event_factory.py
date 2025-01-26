from src.gym_management.domain.admin.events.subscription_unset_event import SubscriptionUnsetEvent
from src.gym_management.domain.subscription.aggregate_root import Subscription
from tests.common.gym_management.subscription.factory.subscription_factory import SubscriptionFactory


class SubscriptionDomainEventFactory:
    @staticmethod
    def create_subscription_unset_event(
        subscription: Subscription | None = None,
    ) -> SubscriptionUnsetEvent:
        if subscription is None:
            subscription = SubscriptionFactory.create_subscription()
        return SubscriptionUnsetEvent(subscription=subscription)
