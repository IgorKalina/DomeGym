import logging

import orjson
from dependency_injector import providers
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from src.gym_management.infrastructure.common.config.database import DatabaseConfig
from src.gym_management.infrastructure.common.injection.containers.repository_base import RepositoryContainer
from src.gym_management.infrastructure.common.postgres.repository.admin import (
    AdminPostgresRepository,
)
from src.gym_management.infrastructure.common.postgres.repository.gym import GymPostgresRepository
from src.gym_management.infrastructure.common.postgres.repository.room import RoomPostgresRepository
from src.gym_management.infrastructure.common.postgres.repository.subscription import (
    SubscriptionPostgresRepository,
)
from src.shared_kernel.infrastructure.event.failed_events_tinydb_repository import (
    FailedDomainEventTinyDBRepository,
)

logger = logging.getLogger(__name__)


async def _init_engine(config: DatabaseConfig) -> AsyncEngine:
    engine = create_async_engine(
        url=config.full_url,
        echo_pool=True,
        json_serializer=lambda data: orjson.dumps(data).decode(),
        json_deserializer=orjson.loads,
        pool_size=50,
    )
    try:
        yield engine
    finally:
        await engine.dispose()


def _init_session(engine: AsyncEngine) -> AsyncSession:
    session_factory = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    session = session_factory()
    logger.info("Postgres session has been established")
    return session


class RepositoryPostgresContainer(RepositoryContainer):
    config: providers.Dependency[DatabaseConfig] = providers.Dependency()
    engine = providers.Resource(_init_engine, config=config)
    session_provider = providers.Singleton(_init_session, engine=engine)

    admin_repository = providers.Factory(AdminPostgresRepository, session=session_provider)
    subscription_repository = providers.Factory(SubscriptionPostgresRepository, session=session_provider)
    gym_repository = providers.Factory(GymPostgresRepository, session=session_provider)
    room_repository = providers.Factory(RoomPostgresRepository, session=session_provider)
    failed_domain_event_repository = providers.Factory(FailedDomainEventTinyDBRepository)
