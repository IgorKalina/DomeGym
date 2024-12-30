import uuid

from src.gym_management.application.subscription.commands.create_subscription import CreateSubscription
from src.gym_management.domain.subscription.subscription_type import SubscriptionType
from tests.common.gym_management import constants


class SubscriptionCommandFactory:
    @staticmethod
    def create_create_subscription_command(
        admin_id: uuid.UUID = constants.admin.ADMIN_ID,
        subscription_type: SubscriptionType = constants.subscription.DEFAULT_SUBSCRIPTION_TYPE,
    ) -> CreateSubscription:
        return CreateSubscription(admin_id=admin_id, subscription_type=subscription_type)
