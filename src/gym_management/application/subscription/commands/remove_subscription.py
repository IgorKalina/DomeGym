import uuid
from typing import TYPE_CHECKING, List

from src.gym_management.application.common import dto
from src.gym_management.application.common.dto.repository.subscription import SubscriptionDB
from src.gym_management.application.common.interfaces.repository.admin_repository import AdminRepository
from src.gym_management.application.common.interfaces.repository.gym_repository import GymRepository
from src.gym_management.application.common.interfaces.repository.subscription_repository import SubscriptionRepository
from src.gym_management.application.subscription.exceptions import (
    SubscriptionDoesNotExistError,
    SubscriptionDoesNotHaveAdminError,
)
from src.shared_kernel.application.command import Command, CommandHandler
from src.shared_kernel.application.event.domain.eventbus import DomainEventBus

if TYPE_CHECKING:
    from src.gym_management.application.common.dto.repository.admin import AdminDB
    from src.gym_management.application.common.dto.repository.gym import GymDB


class RemoveSubscription(Command):
    subscription_id: uuid.UUID


class RemoveSubscriptionHandler(CommandHandler):
    def __init__(
        self,
        admin_repository: AdminRepository,
        subscription_repository: SubscriptionRepository,
        gym_repository: GymRepository,
        eventbus: DomainEventBus,
    ) -> None:
        self.__admin_repository = admin_repository
        self.__subscription_repository = subscription_repository
        self.__gyms_repository = gym_repository
        self.__eventbus = eventbus

    async def handle(self, command: RemoveSubscription) -> SubscriptionDB:
        subscription_db: SubscriptionDB | None = await self.__subscription_repository.get_by_id(command.subscription_id)
        if subscription_db is None:
            raise SubscriptionDoesNotExistError()
        gyms: List[GymDB] = await self.__gyms_repository.get_by_subscription_id(subscription_db.id)

        admin_db: AdminDB | None = await self.__admin_repository.get_by_id(subscription_db.admin_id)
        if admin_db is None:
            raise SubscriptionDoesNotHaveAdminError()

        admin = dto.mappers.map_admin_dto_to_domain(admin_db)
        subscription = dto.mappers.map_subscription_dto_to_domain(subscription=subscription_db, gyms=gyms)
        admin.remove_subscription(subscription)

        admin_db = dto.mappers.map_admin_domain_to_db_dto(admin)
        await self.__subscription_repository.delete(subscription_db)
        await self.__admin_repository.update(admin_db)
        await self.__eventbus.publish(admin.pop_domain_events())
        return subscription_db
