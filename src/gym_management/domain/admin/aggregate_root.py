import uuid
from typing import Optional

from src.gym_management.domain.admin.events.subscription_set_event import SubscriptionSetEvent
from src.gym_management.domain.common.aggregate_root import AggregateRoot
from src.gym_management.domain.subscription.aggregate_root import Subscription


class Admin(AggregateRoot):
    def __init__(
        self,
        *,
        user_id: uuid.UUID,
        subscription_id: uuid.UUID | None = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self.user_id = user_id
        self.__subscription_id = subscription_id

    @property
    def subscription_id(self) -> Optional[uuid.UUID]:
        return self.__subscription_id

    def set_subscription(self, subscription: Subscription) -> None:
        self.__subscription_id = subscription.id
        self._create_domain_event(SubscriptionSetEvent(subscription=subscription))
