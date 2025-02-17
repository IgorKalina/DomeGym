import uuid
from typing import List

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.gym_management.application.common.interfaces.repository.gym_repository import GymRepository
from src.gym_management.application.gym.exceptions import GymDoesNotExistError
from src.gym_management.domain.gym.aggregate_root import Gym
from src.gym_management.infrastructure.common.postgres import models
from src.gym_management.infrastructure.common.postgres.repository.sqlalchemy_repository import SQLAlchemyRepository


class GymPostgresRepository(SQLAlchemyRepository, GymRepository):
    async def get(self, gym_id: uuid.UUID) -> Gym:
        gym: Gym | None = await self.get_or_none(gym_id)
        if gym is None:
            raise GymDoesNotExistError(gym_id=gym_id)
        return gym

    async def get_or_none(self, gym_id: uuid.UUID) -> Gym | None:
        query = (
            select(models.Gym)
            .where(models.Gym.id == gym_id)
            .options(selectinload(models.Gym.room_ids))
            .options(selectinload(models.Gym.trainer_ids))
        )
        result = await self._session.scalars(query)
        gym: models.Gym | None = result.one_or_none()
        if gym is not None:
            return gym.to_domain()
        return None

    async def create(self, gym: Gym) -> None:
        gym_model: models.Gym = models.Gym.from_domain(gym)
        room_ids: List[models.GymRoomIds] = models.GymRoomIds.from_domain(gym)
        trainer_ids: List[models.GymTrainerIds] = models.GymTrainerIds.from_domain(gym)
        self._session.add_all([gym_model, *room_ids, *trainer_ids])
        await self._session.flush((gym_model,))
        await self._session.commit()

    async def get_by_subscription_id(self, subscription_id: uuid.UUID) -> List[Gym]:
        query = (
            select(models.Gym)
            .where(models.Gym.subscription_id == subscription_id)
            .options(selectinload(models.Gym.room_ids))
            .options(selectinload(models.Gym.trainer_ids))
        )
        result: List[models.Gym] = await self._session.scalars(query)
        return [gym.to_domain() for gym in result]

    async def update(self, gym: Gym) -> Gym:
        subscription_model: models.Gym = await self._session.get(models.Gym, gym.id)
        if not subscription_model:
            raise GymDoesNotExistError(gym_id=gym.id)

        gym_model_updated: models.Gym = models.Gym.from_domain(gym)
        gym_model_updated.room_ids = models.GymRoomIds.from_domain(gym)
        gym_model_updated.trainer_ids = models.GymTrainerIds.from_domain(gym)
        await self._session.merge(gym_model_updated)
        await self._session.commit()
        return gym

    async def delete(self, gym: Gym) -> None:
        gym_model: models.Gym = await self._session.get(models.Gym, gym.id)
        if not gym_model:
            raise GymDoesNotExistError(gym_id=gym.id)
        await self._session.delete(gym_model)
        await self._session.commit()
