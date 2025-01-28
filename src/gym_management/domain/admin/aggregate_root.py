import uuid

from src.gym_management.domain.admin.events.subscription_set_event import SubscriptionSetEvent
from src.gym_management.domain.admin.events.subscription_unset_event import SubscriptionUnsetEvent
from src.gym_management.domain.admin.exceptions import AdminDoesNotHaveSubscriptionSetError
from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.shared_kernel.domain.common.aggregate_root import AggregateRoot


class Admin(AggregateRoot):
    user_id: uuid.UUID
    subscription_id: uuid.UUID | None = None

    def set_subscription(self, subscription: Subscription) -> None:
        self.subscription_id = subscription.id
        self._create_domain_event(SubscriptionSetEvent(subscription=subscription.model_copy()))

    def unset_subscription(self, subscription: Subscription) -> None:
        if self.subscription_id is None:
            raise AdminDoesNotHaveSubscriptionSetError()
        self.subscription_id = None
        self._create_domain_event(SubscriptionUnsetEvent(subscription=subscription.model_copy()))


SubscriptionSetEvent.model_rebuild()
SubscriptionUnsetEvent.model_rebuild()
