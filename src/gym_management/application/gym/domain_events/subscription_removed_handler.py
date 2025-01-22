import logging
from typing import TYPE_CHECKING, List

from src.gym_management.application.common.dto.repository.gym import GymDB
from src.gym_management.application.common.interfaces.repository.gym_repository import GymRepository
from src.gym_management.application.common.interfaces.repository.room_repository import RoomRepository
from src.gym_management.domain.admin.events.subscription_removed_event import SubscriptionRemovedEvent
from src.gym_management.domain.gym.aggregate_root import Gym
from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.shared_kernel.application.event.domain.eventbus import DomainEventBus
from src.shared_kernel.domain.event import DomainEventHandler

if TYPE_CHECKING:
    from src.gym_management.application.common.dto.repository.room import RoomDB

logger = logging.getLogger(__name__)


class SubscriptionRemovedHandler(DomainEventHandler):
    """
    Remove all gyms per subscription
    """

    def __init__(
        self, gym_repository: GymRepository, room_repository: RoomRepository, eventbus: DomainEventBus
    ) -> None:
        self.__gym_repository = gym_repository
        self.__room_repository = room_repository
        self.__eventbus = eventbus

    async def handle(self, event: SubscriptionRemovedEvent) -> None:
        logger.info(f"Removing all gyms for the removed subscription with id: {event.subscription.id}")
        gyms: List[GymDB] = await self.__gym_repository.get_by_subscription_id(event.subscription.id)
        subscription = event.subscription
        for gym_db in gyms:
            await self.__remove_gym(subscription=subscription, gym_db=gym_db)

    async def __remove_gym(self, subscription: Subscription, gym_db: GymDB) -> None:
        rooms: List[RoomDB] = await self.__room_repository.get_by_gym_id(gym_db.id)
        gym = Gym(
            id=gym_db.id,
            name=gym_db.name,
            subscription_id=subscription.id,
            max_rooms=subscription.max_rooms,
            room_ids=[room.id for room in rooms],
            created_at=gym_db.created_at,
        )
        subscription.remove_gym(gym)
        await self.__gym_repository.delete(gym_db)
        await self.__eventbus.publish(subscription.pop_domain_events())
        logger.info(f"Removed gym with id: {gym_db.id}")
