import uuid
from typing import List

from sqlalchemy import select

from src.gym_management.application.common.interfaces.repository.gym_repository import GymRepository
from src.gym_management.application.gym.dto.repository import GymDB
from src.gym_management.infrastructure.common.postgres import models
from src.gym_management.infrastructure.common.postgres.repository.sqlalchemy_repository import SQLAlchemyRepository


class GymPostgresRepository(SQLAlchemyRepository, GymRepository):
    async def get_by_id(self, gym_id: uuid.UUID) -> GymDB | None:
        query = select(models.Gym).where(models.Gym.id == gym_id)
        result = await self._session.scalars(query)
        gym: models.Gym = result.one_or_none()
        return gym.to_dto() if gym else None

    async def create(self, gym: GymDB) -> None:
        gym = models.Gym.from_dto(gym)
        self._session.add(gym)
        await self._session.flush((gym,))
        await self._session.commit()

    async def get_by_subscription_id(self, subscription_id: uuid.UUID) -> List[GymDB]:
        query = select(models.Gym).where(models.Gym.subscription_id == subscription_id)
        result: List[models.Gym] = await self._session.scalars(query)
        return [gym.to_dto() for gym in result]
