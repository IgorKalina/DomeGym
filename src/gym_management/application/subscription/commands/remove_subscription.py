import uuid
from typing import TYPE_CHECKING

from src.gym_management.application.common.interfaces.repository.admin_repository import AdminRepository
from src.gym_management.application.common.interfaces.repository.subscription_repository import SubscriptionRepository
from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.gym_management.infrastructure.common.postgres.repository.domain_event import (
    DomainEventPostgresRepository,
)
from src.shared_kernel.application.command import Command, CommandHandler

if TYPE_CHECKING:
    from src.gym_management.domain.admin.aggregate_root import Admin


class RemoveSubscription(Command):
    subscription_id: uuid.UUID


class RemoveSubscriptionHandler(CommandHandler):
    def __init__(
        self,
        subscription_repository: SubscriptionRepository,
        admin_repository: AdminRepository,
        domain_event_repository: DomainEventPostgresRepository,
    ) -> None:
        self.__admin_repository = admin_repository
        self.__subscription_repository = subscription_repository
        self.__domain_event_repository = domain_event_repository

    async def handle(self, command: RemoveSubscription) -> Subscription:
        subscription: Subscription = await self.__subscription_repository.get(command.subscription_id)
        admin: Admin = await self.__admin_repository.get(subscription.admin_id)
        admin.unset_subscription(subscription)

        await self.__admin_repository.update(admin)
        await self.__domain_event_repository.bulk_create(admin.pop_domain_events())
        return subscription
