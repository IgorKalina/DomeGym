import datetime
import uuid

from src.gym_management.domain.subscription.subscription_type import SubscriptionType
from src.gym_management.presentation.api.controllers.common.responses.base import Response


class SubscriptionResponse(Response):
    id: uuid.UUID
    type: SubscriptionType
    created_at: datetime.datetime
    admin_id: uuid.UUID
