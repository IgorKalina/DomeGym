import uuid
from typing import TYPE_CHECKING

from src.gym_management.application.common import dto
from src.gym_management.application.common.dto.repository.subscription import SubscriptionDB
from src.gym_management.application.common.interfaces.repository.admin_repository import AdminRepository
from src.gym_management.application.common.interfaces.repository.subscription_repository import SubscriptionRepository
from src.gym_management.application.subscription.exceptions import (
    SubscriptionDoesNotExistError,
    SubscriptionDoesNotHaveAdminError,
)
from src.gym_management.domain.admin.aggregate_root import Admin
from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.shared_kernel.application.command import Command, CommandHandler
from src.shared_kernel.application.event.domain.eventbus import DomainEventBus

if TYPE_CHECKING:
    from src.gym_management.application.common.dto.repository.admin import AdminDB


class RemoveSubscription(Command):
    subscription_id: uuid.UUID


class RemoveSubscriptionHandler(CommandHandler):
    def __init__(
        self,
        admin_repository: AdminRepository,
        subscription_repository: SubscriptionRepository,
        eventbus: DomainEventBus,
    ) -> None:
        self.__admin_repository = admin_repository
        self.__subscription_repository = subscription_repository
        self.__eventbus = eventbus

    async def handle(self, command: RemoveSubscription) -> SubscriptionDB:
        subscription: Subscription = await self.__get_subscription_domain(command)
        admin: Admin = await self.__get_admin_domain(subscription)
        admin.unset_subscription(subscription)

        await self.__update_admin_in_db(admin)
        subscription_db: SubscriptionDB = await self.__delete_subscription_from_db(subscription)
        await self.__create_domain_events_in_db(admin)
        return subscription_db

    async def __get_subscription_domain(self, command: RemoveSubscription) -> Subscription:
        subscription_db: SubscriptionDB | None = await self.__subscription_repository.get_by_id(command.subscription_id)
        if subscription_db is None:
            raise SubscriptionDoesNotExistError()
        return dto.mappers.subscription.db_to_domain(subscription_db)

    async def __get_admin_domain(self, subscription: Subscription) -> Admin:
        admin_db: AdminDB | None = await self.__admin_repository.get_by_id(subscription.admin_id)
        if admin_db is None:
            raise SubscriptionDoesNotHaveAdminError()
        return dto.mappers.admin.db_to_domain(admin_db)

    async def __update_admin_in_db(self, admin: Admin) -> None:
        admin_db: AdminDB = dto.mappers.admin.domain_to_db(admin)
        await self.__admin_repository.update(admin_db)

    async def __delete_subscription_from_db(self, subscription: Subscription) -> SubscriptionDB:
        subscription_db: SubscriptionDB = dto.mappers.subscription.domain_to_db(subscription)
        await self.__subscription_repository.delete(subscription)
        return subscription_db

    async def __create_domain_events_in_db(self, admin: Admin) -> None:
        await self.__eventbus.publish(admin.pop_domain_events())
