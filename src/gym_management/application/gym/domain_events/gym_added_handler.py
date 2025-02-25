import logging
from typing import TYPE_CHECKING

from src.gym_management.application.common.interfaces.repository.domain_event_outbox_repository import (
    DomainEventRepository,
)
from src.gym_management.application.common.interfaces.repository.gym_repository import GymRepository
from src.gym_management.domain.subscription.events.gym_added_event import GymAddedEvent, SomeEvent
from src.shared_kernel.domain.common.event import DomainEventHandler

if TYPE_CHECKING:
    from src.gym_management.domain.gym.aggregate_root import Gym

logger = logging.getLogger(__name__)


class GymAddedEventHandler(DomainEventHandler):
    def __init__(
        self,
        gym_repository: GymRepository,
        domain_event_repository: DomainEventRepository,
    ) -> None:
        self.__gym_repository = gym_repository
        self.__domain_event_repository = domain_event_repository

    async def handle(self, event: GymAddedEvent) -> None:
        existing_gym: Gym | None = await self.__gym_repository.get_or_none(event.gym.id)
        if existing_gym is not None:
            logger.warning(f"Gym with id '{event.gym.id}' already exists")
            return
        await self.__gym_repository.create(event.gym)
        await self.__domain_event_repository.bulk_create([SomeEvent()])
