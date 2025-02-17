import logging

from src.gym_management.application.common.interfaces.repository.room_repository import RoomRepository
from src.gym_management.domain.gym.events.room_removed_event import RoomRemovedEvent
from src.shared_kernel.domain.common.event import DomainEventHandler

logger = logging.getLogger(__name__)


class RoomRemovedHandler(DomainEventHandler):
    """
    Removes all rooms per gym
    """

    def __init__(
        self,
        room_repository: RoomRepository,
    ) -> None:
        self.__room_repository = room_repository

    async def handle(self, event: RoomRemovedEvent) -> None:
        await self.__room_repository.delete(event.room_id)
        logger.info(f"Removed room with id: {event.room_id}")
