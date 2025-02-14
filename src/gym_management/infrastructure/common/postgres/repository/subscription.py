import uuid
from typing import TYPE_CHECKING, List

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.gym_management.application.common.interfaces.repository.subscription_repository import SubscriptionRepository
from src.gym_management.application.subscription.exceptions import SubscriptionDoesNotExistError
from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.gym_management.infrastructure.common import dto
from src.gym_management.infrastructure.common.postgres import models
from src.gym_management.infrastructure.common.postgres.repository.sqlalchemy_repository import SQLAlchemyRepository

if TYPE_CHECKING:
    from src.gym_management.application.common.dto.repository.subscription import SubscriptionDB


class SubscriptionPostgresRepository(SQLAlchemyRepository, SubscriptionRepository):
    async def create(self, subscription: Subscription) -> None:
        subscription_db: SubscriptionDB = dto.mappers.subscription.domain_to_db(subscription)
        subscription_model: models.Subscription = models.Subscription.from_dto(subscription_db)
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
            .options(selectinload(models.Subscription.gyms))
        )
        result = await self._session.scalars(query)
        subscription: models.Subscription = result.one_or_none()
        if subscription:
            return dto.mappers.subscription.db_to_domain(subscription.to_dto())
        return None

    async def get_by_admin_id(self, admin_id: uuid.UUID) -> Subscription:
        query = (
            select(models.Subscription)
            .where(models.Subscription.admin_id == admin_id)
            .options(selectinload(models.Subscription.gyms))
        )
        result = await self._session.scalars(query)
        subscription: models.Subscription = result.one_or_none()
        if subscription is None:
            raise SubscriptionDoesNotExistError()
        return dto.mappers.subscription.db_to_domain(subscription.to_dto())

    async def get_multi(self) -> List[Subscription]:
        query = select(models.Subscription).options(selectinload(models.Subscription.gyms))
        result: List[models.Subscription] = await self._session.scalars(query)
        return [dto.mappers.subscription.db_to_domain(subscription.to_dto()) for subscription in result]

    async def update(self, subscription: Subscription) -> Subscription:
        subscription_model: models.Subscription = await self._session.get(models.Subscription, subscription.id)
        if not subscription_model:
            raise SubscriptionDoesNotExistError()

        subscription_db: SubscriptionDB = dto.mappers.subscription.domain_to_db(subscription)
        subscription_model_updated: models.Subscription = models.Subscription.from_dto(subscription_db)
        await self._session.merge(subscription_model_updated)
        await self._session.commit()
        return subscription

    async def delete(self, subscription: Subscription) -> None:
        subscription_model: models.Subscription = await self._session.get(models.Subscription, subscription.id)
        if not subscription_model:
            raise SubscriptionDoesNotExistError()
        await self._session.delete(subscription_model)
        await self._session.commit()
