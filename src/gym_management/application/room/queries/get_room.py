import uuid

from src.gym_management.application.common.interfaces.repository.gym_repository import GymRepository
from src.gym_management.application.common.interfaces.repository.room_repository import RoomRepository
from src.gym_management.domain.room.aggregate_root import Room
from src.shared_kernel.application.query.interfaces.query import Query, QueryHandler


class GetRoom(Query):
    gym_id: uuid.UUID
    subscription_id: uuid.UUID
    room_id: uuid.UUID


class GetRoomHandler(QueryHandler):
    def __init__(self, room_repository: RoomRepository, gym_repository: GymRepository) -> None:
        self.__room_repository = room_repository
        self.__gym_repository = gym_repository

    async def handle(self, query: GetRoom) -> Room:
        return await self.__room_repository.get(query.room_id)
