import uuid
from typing import List

from src.gym_management.application.common.dto.repository.gym import GymDB
from src.gym_management.application.common.interfaces.repository.gym_repository import GymRepository
from src.shared_kernel.application.query.interfaces.query import Query, QueryHandler


class ListGyms(Query):
    subscription_id: uuid.UUID


class ListGymsHandler(QueryHandler):
    def __init__(self, gym_repository: GymRepository) -> None:
        self.__gym_repository = gym_repository

    async def handle(self, query: ListGyms) -> List[GymDB]:
        return await self.__gym_repository.get_by_subscription_id(query.subscription_id)
