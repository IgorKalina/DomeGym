import uuid
from typing import List

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.gym_management.application.common.interfaces.repository.subscription_repository import SubscriptionRepository
from src.gym_management.application.subscription.exceptions import SubscriptionDoesNotExistError
from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.gym_management.infrastructure.common.postgres import models
from src.gym_management.infrastructure.common.postgres.repository.sqlalchemy_repository import SQLAlchemyRepository


class SubscriptionPostgresRepository(SQLAlchemyRepository, SubscriptionRepository):
    async def create(self, subscription: Subscription) -> None:
        subscription_model: models.Subscription = models.Subscription.from_domain(subscription)
        self._session.add(subscription_model)
        await self._session.flush((subscription_model,))
        await self._session.commit()

    async def get(self, subscription_id: uuid.UUID) -> Subscription:
        subscription: Subscription | None = await self.get_or_none(subscription_id)
        if subscription is None:
            raise SubscriptionDoesNotExistError()
        return subscription

    async def get_or_none(self, subscription_id: uuid.UUID) -> Subscription | None:
        query = (
            select(models.Subscription)
            .where(models.Subscription.id == subscription_id)
            .options(selectinload(models.Subscription.gym_ids))
        )
        result = await self._session.scalars(query)
        subscription: models.Subscription = result.one_or_none()
        if subscription:
            return subscription.to_domain()
        return None

    async def get_by_admin_id(self, admin_id: uuid.UUID) -> Subscription:
        query = (
            select(models.Subscription)
            .where(models.Subscription.admin_id == admin_id)
            .options(selectinload(models.Subscription.gym_ids))
        )
        result = await self._session.scalars(query)
        subscription: models.Subscription = result.one_or_none()
        if subscription is None:
            raise SubscriptionDoesNotExistError()
        return subscription.to_domain()

    async def get_multi(self) -> List[Subscription]:
        query = select(models.Subscription).options(selectinload(models.Subscription.gym_ids))
        result: List[models.Subscription] = await self._session.scalars(query)
        return [subscription.to_domain() for subscription in result]

    async def update(self, subscription: Subscription) -> Subscription:
        subscription_model: models.Subscription = await self._session.get(models.Subscription, subscription.id)
        if not subscription_model:
            raise SubscriptionDoesNotExistError()

        subscription_model_updated: models.Subscription = models.Subscription.from_domain(subscription)
        subscription_model_updated.gym_ids = models.SubscriptionGymIds.from_domain(subscription)
        await self._session.merge(subscription_model_updated)
        await self._session.commit()
        return subscription

    async def delete(self, subscription: Subscription) -> None:
        subscription_model: models.Subscription = await self._session.get(models.Subscription, subscription.id)
        if not subscription_model:
            raise SubscriptionDoesNotExistError()
        await self._session.delete(subscription_model)
        await self._session.commit()
