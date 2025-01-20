import logging

import orjson
from dependency_injector import providers
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from src.gym_management.infrastructure.common.config.database import DatabaseConfig
from src.gym_management.infrastructure.common.injection.containers.repository_base import RepositoryContainer
from src.gym_management.infrastructure.common.postgres.repository.admin.repository_postgres import (
    AdminPostgresRepository,
)
from src.gym_management.infrastructure.common.postgres.repository.gym.repository_postgres import GymPostgresRepository
from src.gym_management.infrastructure.common.postgres.repository.subscription.repository_postgres import (
    SubscriptionPostgresRepository,
)
from src.shared_kernel.infrastructure.event.domain.failed_events_tinydb_repository import (
    FailedDomainEventTinyDBRepository,
)

logger = logging.getLogger(__name__)


def _build_sa_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


async def _init_postgres_session(config: DatabaseConfig) -> AsyncSession:
    engine = create_async_engine(
        url=config.full_url,
        echo=True,
        echo_pool=True,
        json_serializer=lambda data: orjson.dumps(data).decode(),
        json_deserializer=orjson.loads,
        pool_size=50,
    )
    session_factory = _build_sa_session_factory(engine)
    async with session_factory() as session:
        await session.execute(select(1))
        logger.info("Postgres session has been set up successfully")
        yield session

    await engine.dispose()


class RepositoryPostgresContainer(RepositoryContainer):
    config: providers.Dependency[DatabaseConfig] = providers.Dependency()
    session_provider = providers.Resource(_init_postgres_session, config=config)

    admin_repository = providers.Singleton(AdminPostgresRepository, session=session_provider)
    subscription_repository = providers.Singleton(SubscriptionPostgresRepository, session=session_provider)
    gym_repository = providers.Singleton(GymPostgresRepository, session=session_provider)
    failed_domain_event_repository = providers.Singleton(FailedDomainEventTinyDBRepository)
