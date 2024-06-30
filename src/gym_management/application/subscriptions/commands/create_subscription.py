import logging
import uuid
from dataclasses import dataclass

from result import Ok, Result

from src.gym_management.application.common.command import Command, CommandHandler
from src.gym_management.application.common.interfaces.persistence.admins_repository import AdminsRepository
from src.gym_management.application.common.interfaces.persistence.subscriptions_repository import (
    SubscriptionsRepository,
)
from src.gym_management.domain.admin.aggregate_root import Admin
from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.gym_management.domain.subscription.subscription_type import SubscriptionType

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CreateSubscription(Command):
    admin_id: uuid.UUID
    subscription_type: SubscriptionType


class CreateSubscriptionHandler(CommandHandler):
    def __init__(self, admins_repository: AdminsRepository, subscriptions_repository: SubscriptionsRepository) -> None:
        self._admins_repository = admins_repository
        self._subscriptions_repository = subscriptions_repository

    async def handle(self, command: CreateSubscription) -> Result:
        admin = Admin(user_id=command.admin_id)
        await self._admins_repository.create(admin)
        subscription = Subscription(
            admin_id=command.admin_id,
            subscription_type=command.subscription_type,
        )
        await self._subscriptions_repository.create(subscription)
        admin.set_subscription(subscription)
        await self._admins_repository.update(admin)
        return Ok(None)
