import logging
import uuid
from typing import TYPE_CHECKING

from src.gym_management.application.common import dto
from src.gym_management.application.common.dto.repository import RoomDB
from src.gym_management.application.common.dto.repository.gym import GymDB
from src.gym_management.application.common.interfaces.repository.room_repository import RoomRepository
from src.gym_management.application.common.interfaces.repository.subscription_repository import SubscriptionRepository
from src.gym_management.application.gym.queries.get_gym import GetGym
from src.gym_management.application.room.queries.get_room import GetRoom
from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.shared_kernel.application.command import Command, CommandHandler
from src.shared_kernel.application.event.domain.event_bus import DomainEventBus
from src.shared_kernel.application.query.interfaces.query_bus import QueryBus

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
        subscription_repository: SubscriptionRepository,
        query_bus: QueryBus,
        domain_event_bus: DomainEventBus,
    ) -> None:
        self.__room_repository = room_repository
        self.__subscription_repository = subscription_repository

        self.__domain_event_bus = domain_event_bus
        self.__query_bus = query_bus

    async def handle(self, command: RemoveRoom) -> RoomDB:
        subscription: Subscription = await self.__subscription_repository.get(command.subscription_id)
        gym: Gym = await self.__get_gym(command, subscription=subscription)
        room_db: RoomDB = await self.__get_room(command)
        room: Room = dto.mappers.room.db_to_domain(room=room_db, subscription=subscription)
        gym.remove_room(room)

        await self.__room_repository.delete(room_db)
        await self.__domain_event_bus.publish(gym.pop_domain_events())
        logger.info(f"Removed room with id: {room_db.id}")
        return room_db

    async def __get_gym(self, command: RemoveRoom, subscription: Subscription) -> GymDB:
        get_gym_query = GetGym(subscription_id=command.subscription_id, gym_id=command.gym_id)
        gym_db: GymDB = await self.__query_bus.invoke(get_gym_query)
        return dto.mappers.gym.db_to_domain(gym=gym_db, subscription=subscription)

    async def __get_room(self, command: RemoveRoom) -> RoomDB:
        get_room_query = GetRoom(
            gym_id=command.gym_id, subscription_id=command.subscription_id, room_id=command.room_id
        )
        return await self.__query_bus.invoke(get_room_query)
