import datetime
import uuid

from src.gym_management.domain.subscription.subscription_type import SubscriptionType
from src.gym_management.presentation.api.controllers.common.responses.dto import ResponseData


class SubscriptionResponse(ResponseData):
    id: uuid.UUID
    type: SubscriptionType
    admin_id: uuid.UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime
