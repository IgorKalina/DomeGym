import logging
import uuid

from src.gym_management.application.admin.exceptions import AdminAlreadyExistsError
from src.gym_management.application.common import dto
from src.gym_management.application.common.dto.repository.admin import AdminDB
from src.gym_management.application.common.dto.repository.subscription import SubscriptionDB
from src.gym_management.application.common.interfaces.repository.admin_repository import AdminRepository
from src.gym_management.application.common.interfaces.repository.domain_event_outbox_repository import (
    DomainEventOutboxRepository,
)
from src.gym_management.application.common.interfaces.repository.subscription_repository import (
    SubscriptionRepository,
)
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
        subscription_repository: SubscriptionRepository,
        domain_event_outbox_repository: DomainEventOutboxRepository,
    ) -> None:
        self.__admin_repository = admin_repository
        self.__subscription_repository = subscription_repository
        self.__domain_event_outbox_repository = domain_event_outbox_repository

    async def handle(self, command: CreateSubscription) -> SubscriptionDB:
        admin_db: AdminDB | None = await self.__admin_repository.get_by_id(command.admin_id)
        if admin_db is not None:
            raise AdminAlreadyExistsError()

        admin_db = AdminDB(id=command.admin_id, user_id=uuid.uuid4())
        await self.__admin_repository.create(admin_db)

        subscription = Subscription(admin_id=command.admin_id, type=command.subscription_type)
        admin = dto.mappers.admin.db_to_domain(admin_db)
        admin.set_subscription(subscription)

        subscription_db: SubscriptionDB = dto.mappers.subscription.domain_to_db(subscription)
        admin_db = dto.mappers.admin.domain_to_db(admin)
        await self.__subscription_repository.create(subscription_db)
        await self.__admin_repository.update(admin_db)
        domain_events = admin.pop_domain_events()
        await self.__domain_event_outbox_repository.create_multi(
            [dto.repository.DomainEventDB(event=event) for event in domain_events]
        )
        return subscription_db
