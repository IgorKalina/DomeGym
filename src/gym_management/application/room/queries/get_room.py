import uuid

from src.gym_management.application.common.dto.repository import RoomDB
from src.gym_management.application.common.dto.repository.gym import GymDB
from src.gym_management.application.common.interfaces.repository.room_repository import RoomRepository
from src.gym_management.application.gym.queries.get_gym import GetGym
from src.gym_management.domain.room.exceptions import RoomDoesNotExistError
from src.shared_kernel.application.query.interfaces.query import Query, QueryHandler
from src.shared_kernel.application.query.interfaces.query_bus import QueryBus


class GetRoom(Query):
    gym_id: uuid.UUID
    subscription_id: uuid.UUID
    room_id: uuid.UUID


class GetRoomHandler(QueryHandler):
    def __init__(self, room_repository: RoomRepository, query_bus: QueryBus) -> None:
        self.__room_repository = room_repository

        self.__query_bus = query_bus

    async def handle(self, query: GetRoom) -> RoomDB:
        await self.__get_gym(query)

        room: RoomDB | None = await self.__room_repository.get_by_id(query.room_id)
        if room is None:
            raise RoomDoesNotExistError()
        return room

    async def __get_gym(self, query: GetRoom) -> GymDB:
        get_gym_query = GetGym(subscription_id=query.subscription_id, gym_id=query.gym_id)
        return await self.__query_bus.invoke(get_gym_query)
