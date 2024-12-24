import datetime
import uuid

from src.gym_management.domain.subscription.subscription_type import SubscriptionType
from src.gym_management.presentation.api.controllers.common.responses.dto import ResponseData


class SubscriptionResponse(ResponseData):
    id: uuid.UUID
    type: SubscriptionType
    created_at: datetime.datetime
    admin_id: uuid.UUID
