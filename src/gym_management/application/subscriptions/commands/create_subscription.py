import logging
import uuid
from dataclasses import dataclass

from src.gym_management.application.admins.exceptions import AdminAlreadyExistsError
from src.gym_management.application.common.interfaces.repository.admins_repository import AdminsRepository
from src.gym_management.application.common.interfaces.repository.subscriptions_repository import (
    SubscriptionsRepository,
)
from src.gym_management.domain.admin.aggregate_root import Admin
from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.gym_management.domain.subscription.subscription_type import SubscriptionType
from src.shared_kernel.application.command import Command, CommandHandler
from src.shared_kernel.application.event.eventbus import EventBus

logger = logging.getLogger(__name__)


@dataclass(kw_only=True, frozen=True)
class CreateSubscription(Command):
    admin_id: uuid.UUID
    subscription_type: SubscriptionType


class CreateSubscriptionHandler(CommandHandler):
    def __init__(
        self,
        admins_repository: AdminsRepository,
        subscriptions_repository: SubscriptionsRepository,
        eventbus: EventBus,
    ) -> None:
        self.__admins_repository = admins_repository
        self.__subscriptions_repository = subscriptions_repository
        self.__event_bus = eventbus

    async def handle(self, command: CreateSubscription) -> Subscription:
        admin = await self.__admins_repository.get_by_id(command.admin_id)
        if admin is not None:
            raise AdminAlreadyExistsError()

        admin = Admin(id=command.admin_id, user_id=uuid.uuid4())
        await self.__admins_repository.create(admin)
        subscription = Subscription(
            admin_id=command.admin_id,
            subscription_type=command.subscription_type,
        )
        await self.__subscriptions_repository.create(subscription)
        admin.set_subscription(subscription)
        await self.__admins_repository.update(admin)
        await self.__event_bus.publish(admin.pop_domain_events())
        return subscription
