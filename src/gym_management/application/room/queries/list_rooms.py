import uuid
from typing import List

from src.gym_management.application.common.dto.repository import GymDB
from src.gym_management.application.common.dto.repository.room import RoomDB
from src.gym_management.application.common.interfaces.repository.room_repository import RoomRepository
from src.gym_management.application.gym.queries.get_gym import GetGym
from src.shared_kernel.application.query.interfaces.query import Query, QueryHandler
from src.shared_kernel.application.query.interfaces.query_invoker import QueryInvoker


class ListRooms(Query):
    gym_id: uuid.UUID
    subscription_id: uuid.UUID


class ListRoomsHandler(QueryHandler):
    def __init__(
        self,
        query_invoker: QueryInvoker,
        room_repository: RoomRepository,
    ) -> None:
        self.__room_repository = room_repository

        self.__query_invoker = query_invoker

    async def handle(self, query: ListRooms) -> List[RoomDB]:
        gym: GymDB = await self.__get_gym(query)
        return await self.__room_repository.get_by_gym_id(gym_id=gym.id)

    async def __get_gym(self, query: ListRooms) -> GymDB:
        get_gym_query = GetGym(gym_id=query.gym_id, subscription_id=query.subscription_id)
        gym_db: GymDB = await self.__query_invoker.invoke(get_gym_query)
        return gym_db
