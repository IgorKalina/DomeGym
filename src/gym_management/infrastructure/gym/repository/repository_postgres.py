import uuid

from sqlalchemy import select

from src.gym_management.application.common.interfaces.repository.gym_repository import GymRepository
from src.gym_management.application.gym.dto.repository import GymDB
from src.gym_management.infrastructure.common.postgres.repository.sqlalchemy_repository import SQLAlchemyRepository

from ..postgres import models


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
