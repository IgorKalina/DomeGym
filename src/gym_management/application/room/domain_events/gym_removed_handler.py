import logging
from typing import TYPE_CHECKING, List

from src.gym_management.application.common import dto
from src.gym_management.application.common.interfaces.repository.gym_repository import GymRepository
from src.gym_management.application.common.interfaces.repository.room_repository import RoomRepository
from src.gym_management.application.common.interfaces.repository.subscription_repository import SubscriptionRepository
from src.gym_management.domain.subscription.events.gym_removed_event import GymRemovedEvent
from src.shared_kernel.application.event.domain.event_bus import DomainEventBus
from src.shared_kernel.domain.common.event import DomainEventHandler

if TYPE_CHECKING:
    from src.gym_management.application.common.dto.repository.gym import GymDB
    from src.gym_management.domain.gym.aggregate_root import Gym
    from src.gym_management.domain.room.aggregate_root import Room
    from src.gym_management.domain.subscription.aggregate_root import Subscription

logger = logging.getLogger(__name__)


class GymRemovedHandler(DomainEventHandler):
    """
    Removes all rooms per gym
    """

    def __init__(
        self,
        room_repository: RoomRepository,
        gym_repository: GymRepository,
        subscription_repository: SubscriptionRepository,
        domain_event_bus: DomainEventBus,
    ) -> None:
        self.__room_repository = room_repository
        self.__gym_repository = gym_repository
        self.__subscription_repository = subscription_repository
        self.__domain_event_bus = domain_event_bus

    async def handle(self, event: GymRemovedEvent) -> None:
        logger.info(f"Removing all rooms for the removed gym with id: {event.gym.id}")
        await self.__remove_all_rooms_for_gym(event)
        logger.info(f"All rooms have been removed for the gym id: {event.gym.id}")

    async def __remove_all_rooms_for_gym(self, event: GymRemovedEvent) -> None:
        subscription: Subscription = await self.__subscription_repository.get(event.subscription.id)
        rooms: List[GymDB] = await self.__room_repository.get_by_gym_id(event.gym.id)
        gym: Gym = dto.mappers.gym.gym_removed_event_to_domain(event, rooms=rooms)
        for room_db in rooms:
            room: Room = dto.mappers.room.db_to_domain(room=room_db, subscription=subscription)
            gym.remove_room(room)
            await self.__room_repository.delete(room_db)
            logger.info(f"Removed room with id: {room_db.id}")

        await self.__domain_event_bus.publish(gym.pop_domain_events())
