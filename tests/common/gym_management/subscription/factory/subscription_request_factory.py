import uuid

from src.gym_management.domain.subscription.subscription_type import SubscriptionType
from src.gym_management.presentation.api.controllers.subscription.v1.requests.create_subscription_request import (
    CreateSubscriptionRequest,
)
from tests.common.gym_management.common import constants


class SubscriptionRequestFactory:
    @staticmethod
    def create_create_subscription_request(
        admin_id: uuid.UUID = constants.admin.ADMIN_ID,
        subscription_type: SubscriptionType = constants.subscription.DEFAULT_SUBSCRIPTION_TYPE,
    ) -> CreateSubscriptionRequest:
        return CreateSubscriptionRequest(admin_id=admin_id, subscription_type=subscription_type)
