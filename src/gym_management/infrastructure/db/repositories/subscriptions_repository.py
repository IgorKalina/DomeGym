import uuid
from typing import Iterable, List, Optional

from sqlalchemy import select

from src.gym_management.application.common.interfaces.persistence.subscriptions_repository import (
    SubscriptionsRepository,
)
from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.gym_management.infrastructure.db import models
from src.gym_management.infrastructure.db.mappers.subscriptions import (
    map_subscription_db_model_to_domain_model,
    map_subscription_domain_model_to_db_model,
)
from src.gym_management.infrastructure.db.repositories.base.sqlalchemy_repository import SQLAlchemyRepo


class SubscriptionsPostgresRepository(SQLAlchemyRepo, SubscriptionsRepository):
    async def create(self, subscription: Subscription) -> None:
        db_subscription = map_subscription_domain_model_to_db_model(subscription)
        self._session.add(db_subscription)
        await self._session.flush((db_subscription,))
        await self._session.commit()

    async def get_by_id(self, subscription_id: uuid.UUID) -> Optional[Subscription]:  # type: ignore
        pass

    async def get_by_admin_id(self, admin_id: uuid.UUID) -> Optional[Subscription]:  # type: ignore
        pass

    async def get_multi(self) -> List[Subscription]:
        query = select(models.Subscription)
        result: Iterable[models.Subscription] = await self._session.scalars(query)
        subscriptions = [map_subscription_db_model_to_domain_model(subscription) for subscription in result]
        return subscriptions

    async def update(self, subscription: Subscription) -> Subscription:  # type: ignore
        pass
