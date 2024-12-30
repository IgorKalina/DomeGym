import uuid
from dataclasses import dataclass
from typing import Optional

from src.gym_management.domain.admin.events.subscription_set_event import SubscriptionSetEvent
from src.gym_management.domain.common.aggregate_root import AggregateRoot
from src.gym_management.domain.subscription.aggregate_root import Subscription


@dataclass(kw_only=True)
class Admin(AggregateRoot):
    user_id: uuid.UUID
    __subscription_id: uuid.UUID | None = None

    @property
    def subscription_id(self) -> Optional[uuid.UUID]:
        return self.__subscription_id

    def set_subscription(self, subscription: Subscription) -> None:
        self.__subscription_id = subscription.id

        self._create_domain_event(SubscriptionSetEvent(subscription=subscription))
