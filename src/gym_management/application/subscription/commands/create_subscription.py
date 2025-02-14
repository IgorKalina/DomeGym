import logging
import uuid

from src.gym_management.application.admin.exceptions import AdminAlreadyExistsError
from src.gym_management.application.common import dto
from src.gym_management.application.common.dto.repository.admin import AdminDB
from src.gym_management.application.common.interfaces.repository.admin_repository import AdminRepository
from src.gym_management.application.common.interfaces.repository.subscription_repository import (
    SubscriptionRepository,
)
from src.gym_management.domain.admin.aggregate_root import Admin
from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.gym_management.domain.subscription.subscription_type import SubscriptionType
from src.shared_kernel.application.command import Command, CommandHandler
from src.shared_kernel.application.event.domain.event_bus import DomainEventBus

logger = logging.getLogger(__name__)


class CreateSubscription(Command):
    admin_id: uuid.UUID
    subscription_type: SubscriptionType


class CreateSubscriptionHandler(CommandHandler):
    def __init__(
        self,
        admin_repository: AdminRepository,
        subscription_repository: SubscriptionRepository,
        domain_event_bus: DomainEventBus,
    ) -> None:
        self.__admin_repository = admin_repository
        self.__subscription_repository = subscription_repository
        self.__event_bus = domain_event_bus

    async def handle(self, command: CreateSubscription) -> Subscription:
        admin: Admin = await self.__get_admin(command)
        subscription: Subscription = Subscription(admin_id=command.admin_id, type=command.subscription_type)
        admin.set_subscription(subscription)

        await self.__subscription_repository.create(subscription)
        await self.__update_admin_in_db(admin)
        await self.__event_bus.publish(admin.pop_domain_events())
        return subscription

    async def __get_admin(self, command: CreateSubscription) -> Admin:
        admin_db: AdminDB | None = await self.__admin_repository.get_by_id(command.admin_id)
        if admin_db is not None:
            raise AdminAlreadyExistsError()

        admin_db = AdminDB(id=command.admin_id, user_id=uuid.uuid4())
        await self.__admin_repository.create(admin_db)
        return dto.mappers.admin.db_to_domain(admin_db)

    async def __update_admin_in_db(self, admin: Admin) -> None:
        admin_db: AdminDB = dto.mappers.admin.domain_to_db(admin)
        await self.__admin_repository.update(admin_db)
