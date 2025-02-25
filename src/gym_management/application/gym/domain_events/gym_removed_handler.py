import logging
from typing import TYPE_CHECKING, List

from src.gym_management.application.common.interfaces.repository.domain_event_outbox_repository import (
    DomainEventRepository,
)
from src.gym_management.application.common.interfaces.repository.gym_repository import GymRepository
from src.gym_management.application.common.interfaces.repository.room_repository import RoomRepository
from src.gym_management.domain.gym.aggregate_root import Gym
from src.gym_management.domain.subscription.events.gym_removed_event import GymRemovedEvent
from src.shared_kernel.domain.common.event import DomainEventHandler

if TYPE_CHECKING:
    from src.gym_management.domain.room.aggregate_root import Room

logger = logging.getLogger(__name__)


class GymRemovedHandler(DomainEventHandler):
    """
    Removes all rooms per gym
    """

    def __init__(
        self,
        room_repository: RoomRepository,
        gym_repository: GymRepository,
        domain_event_repository: DomainEventRepository,
    ) -> None:
        self.__room_repository = room_repository
        self.__gym_repository = gym_repository
        self.__domain_event_repository = domain_event_repository

    async def handle(self, event: GymRemovedEvent) -> None:
        gym: Gym | None = await self.__gym_repository.get_or_none(event.gym.id)
        if gym is None:
            logger.warning(f"Gym with id '{event.gym.id}' has been already removed")
            return
        await self.__remove_all_rooms(gym)

    async def __remove_all_rooms(self, gym: Gym) -> None:
        logger.info(f"Removing all rooms for the removed gym with id: {gym.id}")
        rooms: List[Room] = await self.__room_repository.get_by_gym_id(gym.id)
        for room in rooms:
            gym.remove_room(room)
            logger.info(f"Removed room with id '{room.id}' from gym id: {gym.id}")

        await self.__domain_event_repository.bulk_create(gym.pop_domain_events())
        await self.__gym_repository.delete(gym)
        logger.info(f"All rooms have been removed for the gym id: {gym.id}")
