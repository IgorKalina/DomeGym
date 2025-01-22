import uuid
from typing import List

from sqlalchemy import select

from src.gym_management.application.common.dto.repository.subscription import SubscriptionDB
from src.gym_management.application.common.interfaces.repository.subscription_repository import SubscriptionRepository
from src.gym_management.application.subscription.exceptions import SubscriptionDoesNotExistError
from src.gym_management.infrastructure.common.postgres import models
from src.gym_management.infrastructure.common.postgres.repository.sqlalchemy_repository import SQLAlchemyRepository


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
            return subscription.to_dto()
        return None

    async def get_by_admin_id(self, admin_id: uuid.UUID) -> SubscriptionDB | None:
        query = select(models.Subscription).where(models.Subscription.admin_id == admin_id)
        result = await self._session.scalars(query)
        subscription: models.Subscription = result.one_or_none()
        if subscription:
            return subscription.to_dto()
        return None

    async def get_multi(self) -> List[SubscriptionDB]:
        query = select(models.Subscription)
        result: List[models.Subscription] = await self._session.scalars(query)
        return [subscription.to_dto() for subscription in result]

    async def update(self, subscription: SubscriptionDB) -> SubscriptionDB:
        subscription_db = await self._session.get(models.Subscription, subscription.id)
        if not subscription_db:
            raise SubscriptionDoesNotExistError()

        subscription_db_updated = models.Subscription.from_dto(subscription)
        for key, value in vars(subscription_db_updated).items():
            setattr(subscription_db, key, value)

        await self._session.commit()
        return subscription_db_updated.to_dto()

    async def delete(self, subscription: SubscriptionDB) -> None:
        subscription_db = await self._session.get(models.Subscription, subscription.id)
        if not subscription_db:
            raise SubscriptionDoesNotExistError()
        await self._session.delete(subscription_db)
        await self._session.commit()
