import logging
from typing import TYPE_CHECKING, List

from src.gym_management.application.common.dto.repository.room import RoomDB
from src.gym_management.application.common.interfaces.repository.room_repository import RoomRepository
from src.gym_management.domain.room.aggregate_root import Room
from src.gym_management.domain.subscription.events.gym_removed_event import GymRemovedEvent
from src.shared_kernel.application.event.domain.eventbus import DomainEventBus
from src.shared_kernel.domain.event import DomainEventHandler

if TYPE_CHECKING:
    from src.gym_management.application.common.dto.repository.gym import GymDB

logger = logging.getLogger(__name__)


class GymRemovedHandler(DomainEventHandler):
    """
    Removes all rooms per gym
    """

    def __init__(self, room_repository: RoomRepository, eventbus: DomainEventBus) -> None:
        self.__room_repository = room_repository
        self.__eventbus = eventbus

    async def handle(self, event: GymRemovedEvent) -> None:
        logger.info(f"Removing all rooms for the removed gym with id: {event.gym.id}")
        rooms: List[GymDB] = await self.__room_repository.get_by_gym_id(event.gym.id)
        for room_db in rooms:
            await self.__remove_room(event=event, room_db=room_db)

    async def __remove_room(self, event: GymRemovedEvent, room_db: RoomDB) -> None:
        room = Room(
            id=room_db.id,
            name=room_db.name,
            gym_id=room_db.gym_id,
            max_daily_sessions=event.subscription.max_daily_sessions,
        )
        event.gym.remove_room(room)
        await self.__room_repository.delete(room_db)
        await self.__eventbus.publish(event.gym.pop_domain_events())
        logger.info(f"Removed room with id: {room_db.id}")
