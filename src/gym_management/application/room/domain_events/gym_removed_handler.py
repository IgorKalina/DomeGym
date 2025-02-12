import logging
from typing import TYPE_CHECKING, List

from src.gym_management.application.common.dto.repository.room import RoomDB
from src.gym_management.application.common.interfaces.repository.room_repository import RoomRepository
from src.gym_management.application.room.commands.remove_room import RemoveRoom
from src.gym_management.domain.subscription.events.gym_removed_event import GymRemovedEvent
from src.shared_kernel.application.command import CommandBus
from src.shared_kernel.domain.common.event import DomainEventHandler

if TYPE_CHECKING:
    from src.gym_management.application.common.dto.repository.gym import GymDB

logger = logging.getLogger(__name__)


class GymRemovedHandler(DomainEventHandler):
    """
    Removes all rooms per gym
    """

    def __init__(self, room_repository: RoomRepository, command_bus: CommandBus) -> None:
        self.__room_repository = room_repository

        self.__command_bus = command_bus

    async def handle(self, event: GymRemovedEvent) -> None:
        logger.info(f"Removing all rooms for the removed gym with id: {event.gym.id}")
        rooms: List[GymDB] = await self.__room_repository.get_by_gym_id(event.gym.id)
        for room_db in rooms:
            await self.__remove_room(room_db)
        logger.info(f"All rooms have been removed for the gym id: {event.gym.id}")

    async def __remove_room(self, room_db: RoomDB) -> None:
        # todo: make it idempotent
        remove_room_command = RemoveRoom(
            subscription_id=room_db.subscription_id, gym_id=room_db.gym_id, room_id=room_db.id
        )
        await self.__command_bus.invoke(remove_room_command)
