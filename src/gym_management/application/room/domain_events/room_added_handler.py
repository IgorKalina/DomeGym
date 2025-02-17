import logging

from src.gym_management.application.common.interfaces.repository.room_repository import RoomRepository
from src.gym_management.domain.gym.events.room_added_event import RoomAddedEvent
from src.shared_kernel.domain.common.event import DomainEventHandler

logger = logging.getLogger(__name__)


class RoomAddedHandler(DomainEventHandler):
    def __init__(self, room_repository: RoomRepository) -> None:
        self.__room_repository = room_repository

    async def handle(self, event: RoomAddedEvent) -> None:
        await self.__room_repository.create(event.room)
        logger.info(f"Created a new room: {event.room}")
