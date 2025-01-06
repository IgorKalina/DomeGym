import uuid
from typing import List

from sqlalchemy import select

from src.gym_management.application.common.interfaces.repository.subscription_repository import SubscriptionRepository
from src.gym_management.application.subscription.exceptions import SubscriptionDoesNotExistError
from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.gym_management.infrastructure.db import models
from src.gym_management.infrastructure.db.mappers.subscription import (
    map_subscription_db_model_to_domain_model,
    map_subscription_domain_model_to_db_model,
)
from src.gym_management.infrastructure.db.repository.sqlalchemy_repository import SQLAlchemyRepository


class SubscriptionPostgresRepository(SQLAlchemyRepository, SubscriptionRepository):
    async def create(self, subscription: Subscription) -> None:
        db_subscription = map_subscription_domain_model_to_db_model(subscription)
        self._session.add(db_subscription)
        await self._session.flush((db_subscription,))
        await self._session.commit()

    async def get_by_id(self, subscription_id: uuid.UUID) -> Subscription | None:
        query = select(models.Subscription).where(models.Subscription.id == subscription_id)
        result = await self._session.scalars(query)
        subscription = result.one_or_none()
        return map_subscription_db_model_to_domain_model(subscription) if subscription else None

    async def get_by_admin_id(self, admin_id: uuid.UUID) -> Subscription | None:
        query = select(models.Subscription).where(models.Subscription.admin_id == admin_id)
        result = await self._session.scalars(query)
        subscription = result.one_or_none()
        return map_subscription_db_model_to_domain_model(subscription) if subscription else None

    async def get_multi(self) -> List[Subscription]:
        query = select(models.Subscription)
        result: List[models.Subscription] = list(await self._session.scalars(query))
        return [map_subscription_db_model_to_domain_model(subscription) for subscription in result]

    async def update(self, subscription: Subscription) -> Subscription:
        db_subscription = await self._session.get(models.Subscription, subscription.id)
        if not db_subscription:
            raise SubscriptionDoesNotExistError()

        updated_subscription = map_subscription_domain_model_to_db_model(subscription)
        for key, value in vars(updated_subscription).items():
            setattr(db_subscription, key, value)

        await self._session.commit()
        return map_subscription_db_model_to_domain_model(db_subscription)
