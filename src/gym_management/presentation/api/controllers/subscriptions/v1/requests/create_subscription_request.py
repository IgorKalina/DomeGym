import uuid

from src.gym_management.domain.subscription.subscription_type import SubscriptionType
from src.gym_management.presentation.api.controllers.common.requests.base import ApiRequest


class CreateSubscriptionRequest(ApiRequest):
    admin_id: uuid.UUID
    subscription_type: SubscriptionType
