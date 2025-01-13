import uuid
from typing import List

from sqlalchemy import select

from src.gym_management.application.common.interfaces.repository.subscription_repository import SubscriptionRepository
from src.gym_management.application.subscription.dto.repository import SubscriptionDB
from src.gym_management.application.subscription.exceptions import SubscriptionDoesNotExistError
from src.gym_management.infrastructure.common.postgres.repository.sqlalchemy_repository import SQLAlchemyRepository

from ...gym.postgres import models as gym_models
from ..postgres import models


class SubscriptionPostgresRepository(SQLAlchemyRepository, SubscriptionRepository):
    async def create(self, subscription: SubscriptionDB) -> None:
        subscription_db = models.Subscription.from_dto(subscription)
        self._session.add(subscription_db)
        await self._session.flush((subscription_db,))
        await self._session.commit()

    async def get_by_id(self, subscription_id: uuid.UUID) -> SubscriptionDB | None:
        query = select(models.Subscription).where(models.Subscription.id == subscription_id)
        result = await self._session.scalars(query)
        subscription: models.Subscription = result.one_or_none()
        if subscription:
            return await self.__map_to_subscription_dto(subscription)
        return None

    async def get_by_admin_id(self, admin_id: uuid.UUID) -> SubscriptionDB | None:
        query = select(models.Subscription).where(models.Subscription.admin_id == admin_id)
        result = await self._session.scalars(query)
        subscription: models.Subscription = result.one_or_none()
        if subscription:
            return await self.__map_to_subscription_dto(subscription)
        return None

    async def get_multi(self) -> List[SubscriptionDB]:
        query = select(models.Subscription)
        result: List[models.Subscription] = list(await self._session.scalars(query))
        return [await self.__map_to_subscription_dto(subscription) for subscription in result]

    async def update(self, subscription: SubscriptionDB) -> SubscriptionDB:
        subscription_db = await self._session.get(models.Subscription, subscription.id)
        if not subscription_db:
            raise SubscriptionDoesNotExistError()

        subscription_db_updated = models.Subscription.from_dto(subscription)
        for key, value in vars(subscription_db_updated).items():
            setattr(subscription_db, key, value)

        await self._session.commit()
        return await self.__map_to_subscription_dto(subscription_db_updated)

    async def __map_to_subscription_dto(self, subscription: models.Subscription) -> SubscriptionDB:
        gym_ids = await self.__get_gym_ids_by_subscription_id(subscription.id)
        return subscription.to_dto(gym_ids=gym_ids)

    async def __get_gym_ids_by_subscription_id(self, subscription_id: uuid.UUID) -> List[uuid.UUID]:
        query = select(gym_models.Gym.id).where(gym_models.Gym.subscription_id == subscription_id)
        result = await self._session.scalars(query)
        return list(result)
