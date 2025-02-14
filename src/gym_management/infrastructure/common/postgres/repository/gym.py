import uuid
from typing import TYPE_CHECKING, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.gym_management.application.common.interfaces.repository.gym_repository import GymRepository
from src.gym_management.application.common.interfaces.repository.subscription_repository import SubscriptionRepository
from src.gym_management.application.gym.exceptions import GymDoesNotExistError
from src.gym_management.domain.gym.aggregate_root import Gym
from src.gym_management.infrastructure.common import dto
from src.gym_management.infrastructure.common.postgres import models
from src.gym_management.infrastructure.common.postgres.repository.sqlalchemy_repository import SQLAlchemyRepository

if TYPE_CHECKING:
    from src.gym_management.application.common.dto.repository import GymDB
    from src.gym_management.domain.subscription.aggregate_root import Subscription


class GymPostgresRepository(SQLAlchemyRepository, GymRepository):
    def __init__(self, session: AsyncSession, subscription_repository: SubscriptionRepository) -> None:
        super().__init__(session)
        self.__subscription_repository = subscription_repository

    async def get(self, gym_id: uuid.UUID) -> Gym:
        gym: Gym | None = await self.get_or_none(gym_id)
        if gym is None:
            raise GymDoesNotExistError()
        return gym

    async def get_or_none(self, gym_id: uuid.UUID) -> Gym | None:
        query = select(models.Gym).where(models.Gym.id == gym_id).options(selectinload(models.Gym.rooms))
        result = await self._session.scalars(query)
        gym: models.Gym | None = result.one_or_none()
        if gym is not None:
            subscription: Subscription = await self.__subscription_repository.get(gym.subscription_id)
            return dto.mappers.gym.db_to_domain(gym=gym.to_dto(), subscription=subscription)
        return None

    async def create(self, gym: Gym) -> None:
        gym_db: GymDB = dto.mappers.gym.domain_to_db(gym)
        gym_model: models.Gym = models.Gym.from_dto(gym_db)
        self._session.add(gym_model)
        await self._session.flush((gym_model,))
        await self._session.commit()

    async def get_by_subscription_id(self, subscription_id: uuid.UUID) -> List[Gym]:
        subscription: Subscription = await self.__subscription_repository.get(subscription_id)
        query = (
            select(models.Gym)
            .where(models.Gym.subscription_id == subscription_id)
            .options(selectinload(models.Gym.rooms))
        )
        result: List[models.Gym] = await self._session.scalars(query)
        return [dto.mappers.gym.db_to_domain(gym=gym.to_dto(), subscription=subscription) for gym in result]

    async def delete(self, gym: Gym) -> None:
        gym_model: models.Gym = await self._session.get(models.Gym, gym.id)
        if not gym_model:
            raise GymDoesNotExistError()
        await self._session.delete(gym_model)
        await self._session.commit()
