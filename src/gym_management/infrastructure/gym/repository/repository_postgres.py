import uuid

from sqlalchemy import select

from src.gym_management.application.common.interfaces.repository.gym_repository import GymRepository
from src.gym_management.domain.gym.aggregate_root import Gym
from src.gym_management.infrastructure.db import models
from src.gym_management.infrastructure.db.mappers.gym import (
    map_gym_db_model_to_domain_model,
    map_gym_domain_model_to_db_model,
)
from src.gym_management.infrastructure.db.repository.sqlalchemy_repository import SQLAlchemyRepository


class GymPostgresRepository(SQLAlchemyRepository, GymRepository):
    async def get_by_id(self, gym_id: uuid.UUID) -> Gym | None:
        query = select(models.Gym).where(models.Gym.id == gym_id)
        result = await self._session.scalars(query)
        gym = result.one_or_none()
        return map_gym_db_model_to_domain_model(gym) if gym else None

    async def create(self, gym: Gym) -> None:
        db_gym = map_gym_domain_model_to_db_model(gym)
        self._session.add(db_gym)
        await self._session.flush((db_gym,))
        await self._session.commit()
