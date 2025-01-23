import uuid

from src.gym_management.application.subscription.commands.create_subscription import CreateSubscription
from src.gym_management.application.subscription.commands.remove_subscription import RemoveSubscription
from src.gym_management.domain.subscription.subscription_type import SubscriptionType
from tests.common.gym_management.common import constants


class SubscriptionCommandFactory:
    @staticmethod
    def create_create_subscription_command(
        admin_id: uuid.UUID = constants.admin.ADMIN_ID,
        subscription_type: SubscriptionType = constants.subscription.DEFAULT_SUBSCRIPTION_TYPE,
    ) -> CreateSubscription:
        return CreateSubscription(admin_id=admin_id, subscription_type=subscription_type)

    @staticmethod
    def create_remove_subscription_command(
        subscription_id: uuid.UUID = constants.subscription.SUBSCRIPTION_ID,
    ) -> RemoveSubscription:
        return RemoveSubscription(subscription_id=subscription_id)
