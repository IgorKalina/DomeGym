import typing
import uuid
from typing import List

from src.gym_management.application.common.dto.repository.room import RoomDB
from src.gym_management.application.common.interfaces.repository.gym_repository import GymRepository
from src.gym_management.application.common.interfaces.repository.room_repository import RoomRepository
from src.gym_management.application.common.interfaces.repository.subscription_repository import SubscriptionRepository
from src.gym_management.application.gym.exceptions import GymDoesNotExistError
from src.gym_management.application.subscription.exceptions import SubscriptionDoesNotExistError
from src.shared_kernel.application.query.interfaces.query import Query, QueryHandler

if typing.TYPE_CHECKING:
    from src.gym_management.application.common.dto.repository.gym import GymDB
    from src.gym_management.application.common.dto.repository.subscription import SubscriptionDB


class ListRooms(Query):
    gym_id: uuid.UUID
    subscription_id: uuid.UUID


class ListRoomsHandler(QueryHandler):
    def __init__(
        self,
        subscription_repository: SubscriptionRepository,
        gym_repository: GymRepository,
        room_repository: RoomRepository,
    ) -> None:
        self.__subscription_repository = subscription_repository
        self.__gym_repository = gym_repository
        self.__room_repository = room_repository

    async def handle(self, query: ListRooms) -> List[RoomDB]:
        subscription: SubscriptionDB | None = await self.__subscription_repository.get_by_id(query.subscription_id)
        if subscription is None:
            raise SubscriptionDoesNotExistError()

        gym: GymDB | None = await self.__gym_repository.get_by_id(
            gym_id=query.gym_id, subscription_id=query.subscription_id
        )
        if gym is None:
            raise GymDoesNotExistError()

        return await self.__room_repository.get_by_gym_id(gym_id=gym.id)
