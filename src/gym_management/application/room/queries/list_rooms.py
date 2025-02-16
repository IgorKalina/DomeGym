import uuid
from typing import TYPE_CHECKING, List

from src.gym_management.application.common.interfaces.repository.gym_repository import GymRepository
from src.gym_management.application.common.interfaces.repository.room_repository import RoomRepository
from src.gym_management.application.common.interfaces.repository.subscription_repository import SubscriptionRepository
from src.gym_management.application.gym.exceptions import GymDoesNotExistError
from src.gym_management.domain.room.aggregate_root import Room
from src.shared_kernel.application.query.interfaces.query import Query, QueryHandler

if TYPE_CHECKING:
    from src.gym_management.domain.subscription.aggregate_root import Subscription


class ListRooms(Query):
    gym_id: uuid.UUID
    subscription_id: uuid.UUID


class ListRoomsHandler(QueryHandler):
    def __init__(
        self,
        room_repository: RoomRepository,
        gym_repository: GymRepository,
        subscription_repository: SubscriptionRepository,
    ) -> None:
        self.__room_repository = room_repository
        self.__gym_repository = gym_repository
        self.__subscription_repository = subscription_repository

    async def handle(self, query: ListRooms) -> List[Room]:
        subscription: Subscription = await self.__subscription_repository.get(query.subscription_id)
        if not subscription.has_gym(query.gym_id):
            raise GymDoesNotExistError()
        return await self.__room_repository.get_by_gym_id(gym_id=query.gym_id)
