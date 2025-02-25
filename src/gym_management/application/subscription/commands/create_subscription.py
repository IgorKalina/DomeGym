import logging
import uuid

from src.gym_management.application.admin.exceptions import AdminAlreadyExistsError
from src.gym_management.application.common.interfaces.repository.admin_repository import AdminRepository
from src.gym_management.application.common.interfaces.repository.domain_event_outbox_repository import (
    DomainEventRepository,
)
from src.gym_management.domain.admin.aggregate_root import Admin
from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.gym_management.domain.subscription.subscription_type import SubscriptionType
from src.shared_kernel.application.command import Command, CommandHandler

logger = logging.getLogger(__name__)


class CreateSubscription(Command):
    admin_id: uuid.UUID
    subscription_type: SubscriptionType


class CreateSubscriptionHandler(CommandHandler):
    def __init__(
        self,
        admin_repository: AdminRepository,
        domain_event_repository: DomainEventRepository,
    ) -> None:
        self.__admin_repository = admin_repository
        self.__domain_event_repository = domain_event_repository

    async def handle(self, command: CreateSubscription) -> Subscription:
        admin: Admin = await self.__get_or_create_admin(command)
        subscription: Subscription = Subscription(admin_id=command.admin_id, type=command.subscription_type)
        admin.set_subscription(subscription)

        await self.__admin_repository.update(admin)
        await self.__domain_event_repository.bulk_create(admin.pop_domain_events())
        return subscription

    async def __get_or_create_admin(self, command: CreateSubscription) -> Admin:
        admin: Admin | None = await self.__admin_repository.get_or_none(command.admin_id)
        if admin is not None:
            raise AdminAlreadyExistsError()

        admin = Admin(id=command.admin_id, user_id=uuid.uuid4())
        await self.__admin_repository.create(admin)
        return admin
