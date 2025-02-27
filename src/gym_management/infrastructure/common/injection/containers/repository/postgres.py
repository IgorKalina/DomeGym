import logging

import orjson
from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from src.gym_management.infrastructure.common.config.database import DatabaseConfig
from src.gym_management.infrastructure.common.injection.containers.repository.base import RepositoryContainer
from src.gym_management.infrastructure.common.postgres.repository.admin import (
    AdminPostgresRepository,
)
from src.gym_management.infrastructure.common.postgres.repository.domain_event import (
    DomainEventPostgresRepository,
)
from src.gym_management.infrastructure.common.postgres.repository.gym import GymPostgresRepository
from src.gym_management.infrastructure.common.postgres.repository.room import RoomPostgresRepository
from src.gym_management.infrastructure.common.postgres.repository.subscription import (
    SubscriptionPostgresRepository,
)
from src.gym_management.infrastructure.common.postgres.unit_of_work import SQLAlchemyUnitOfWork
from src.gym_management.presentation.api.controllers.common.responses.orjson import additionally_serialize

logger = logging.getLogger(__name__)


async def _init_engine(config: DatabaseConfig) -> AsyncEngine:
    engine = create_async_engine(
        url=config.get_full_url(safe=False),
        echo_pool=True,
        json_serializer=lambda data: orjson.dumps(data, default=additionally_serialize).decode(),
        json_deserializer=orjson.loads,
        pool_size=50,
    )
    try:
        logger.debug(f"Connected to Postgres engine: {config.get_full_url()}")
        yield engine
    finally:
        await engine.dispose()
        logger.debug(f"Disconnected Postgres engine: {config.get_full_url()}")


def _create_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


async def _init_session(session_factory: async_sessionmaker[AsyncSession]) -> AsyncSession:
    return session_factory()


@containers.copy(RepositoryContainer)
class RepositoryPostgresContainer(RepositoryContainer):
    config: providers.Dependency[DatabaseConfig] = providers.Dependency()

    engine = providers.Resource(_init_engine, config=config)
    session_factory = providers.Factory(_create_session_factory, engine=engine)
    session = providers.ThreadSafeSingleton(_init_session, session_factory=session_factory)
    unit_of_work = providers.Factory(SQLAlchemyUnitOfWork, session=session)

    admin_repository = providers.Factory(AdminPostgresRepository, session=session)
    subscription_repository = providers.Factory(SubscriptionPostgresRepository, session=session)
    gym_repository = providers.Factory(GymPostgresRepository, session=session)
    room_repository = providers.Factory(RoomPostgresRepository, session=session)
    domain_event_repository = providers.Factory(DomainEventPostgresRepository, session=session)
