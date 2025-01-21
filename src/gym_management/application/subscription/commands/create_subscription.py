import logging
import uuid

from src.gym_management.application.admin.dto.repository import AdminDB
from src.gym_management.application.admin.exceptions import AdminAlreadyExistsError
from src.gym_management.application.common.interfaces.repository.admin_repository import AdminRepository
from src.gym_management.application.common.interfaces.repository.subscription_repository import (
    SubscriptionRepository,
)
from src.gym_management.application.subscription.dto.repository import SubscriptionDB
from src.gym_management.domain.admin.aggregate_root import Admin
from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.gym_management.domain.subscription.subscription_type import SubscriptionType
from src.shared_kernel.application.command import Command, CommandHandler
from src.shared_kernel.application.event.domain.eventbus import DomainEventBus

logger = logging.getLogger(__name__)


class CreateSubscription(Command):
    admin_id: uuid.UUID
    subscription_type: SubscriptionType


class CreateSubscriptionHandler(CommandHandler):
    def __init__(
        self,
        admin_repository: AdminRepository,
        subscription_repository: SubscriptionRepository,
        eventbus: DomainEventBus,
    ) -> None:
        self.__admin_repository = admin_repository
        self.__subscription_repository = subscription_repository
        self.__event_bus = eventbus

    async def handle(self, command: CreateSubscription) -> Subscription:
        admin_db: AdminDB | None = await self.__admin_repository.get_by_id(command.admin_id)
        if admin_db is not None:
            raise AdminAlreadyExistsError()

        admin_db = AdminDB(id=command.admin_id, user_id=uuid.uuid4())
        await self.__admin_repository.create(admin_db)

        subscription = Subscription(admin_id=command.admin_id, type=command.subscription_type)
        admin = Admin(id=admin_db.id, user_id=admin_db.user_id, subscription_id=admin_db.subscription_id)
        admin.set_subscription(subscription)

        subscription_db = SubscriptionDB(id=subscription.id, type=subscription.type, admin_id=subscription.admin_id)
        admin_db = AdminDB(id=admin.id, user_id=admin.user_id, subscription_id=subscription_db.id)
        await self.__subscription_repository.create(subscription_db)
        await self.__admin_repository.update(admin_db)
        await self.__event_bus.publish(admin.pop_domain_events())
        return subscription
