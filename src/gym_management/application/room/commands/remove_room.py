import logging
import uuid
from typing import TYPE_CHECKING

from src.gym_management.application.common.dto.repository import RoomDB
from src.gym_management.application.common.interfaces.repository.domain_event_outbox_repository import (
    DomainEventRepository,
)
from src.gym_management.application.common.interfaces.repository.gym_repository import GymRepository
from src.gym_management.application.common.interfaces.repository.room_repository import RoomRepository
from src.gym_management.application.common.interfaces.repository.subscription_repository import SubscriptionRepository
from src.shared_kernel.application.command import Command, CommandHandler

if TYPE_CHECKING:
    from src.gym_management.domain.gym.aggregate_root import Gym
    from src.gym_management.domain.room.aggregate_root import Room

logger = logging.getLogger(__name__)


class RemoveRoom(Command):
    subscription_id: uuid.UUID
    gym_id: uuid.UUID
    room_id: uuid.UUID


class RemoveRoomHandler(CommandHandler):
    def __init__(
        self,
        room_repository: RoomRepository,
        gym_repository: GymRepository,
        subscription_repository: SubscriptionRepository,
        domain_event_repository: DomainEventRepository,
    ) -> None:
        self.__room_repository = room_repository
        self.__gym_repository = gym_repository
        self.__subscription_repository = subscription_repository
        self.__domain_event_repository = domain_event_repository

    async def handle(self, command: RemoveRoom) -> RoomDB:
        await self.__subscription_repository.get(command.subscription_id)
        gym: Gym = await self.__gym_repository.get(command.gym_id)
        room: Room = await self.__room_repository.get(command.room_id)
        gym.remove_room(room)

        await self.__gym_repository.update(gym)
        await self.__domain_event_repository.bulk_create(gym.pop_domain_events())
        logger.info(f"Removed room with id: {room.id}")
        return room
