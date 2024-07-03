import datetime
import uuid

from pydantic import BaseModel

from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.gym_management.domain.subscription.subscription_type import SubscriptionType


class SubscriptionResponse(BaseModel):
    id: uuid.UUID
    type: SubscriptionType
    created_at: datetime.datetime
    admin_id: uuid.UUID

    @classmethod
    def from_domain_model(cls, subscription: Subscription) -> "SubscriptionResponse":
        return cls(
            id=subscription.id,
            type=subscription.type,
            admin_id=subscription.admin_id,
            created_at=subscription.created_at,
        )
