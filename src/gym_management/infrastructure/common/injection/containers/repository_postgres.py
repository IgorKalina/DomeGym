import orjson
from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from src.gym_management.infrastructure.admin.repository.repository_postgres import AdminPostgresRepository
from src.gym_management.infrastructure.common.config import load_config
from src.gym_management.infrastructure.gym.repository.repository_postgres import GymPostgresRepository
from src.gym_management.infrastructure.subscription.repository.repository_postgres import SubscriptionPostgresRepository
from src.shared_kernel.infrastructure.event.domain.failed_events_tinydb_repository import (
    FailedDomainEventTinyDBRepository,
)


def _build_sa_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


async def _init_postgres_session() -> AsyncSession:
    config = load_config()
    engine = create_async_engine(
        url=config.database.full_url,
        echo=True,
        echo_pool=True,
        json_serializer=lambda data: orjson.dumps(data).decode(),
        json_deserializer=orjson.loads,
        pool_size=50,
    )
    session_factory = _build_sa_session_factory(engine)
    async with session_factory() as session:
        yield session

    await engine.dispose()


session_provider = providers.Resource(_init_postgres_session)


class RepositoryPostgresContainer(containers.DeclarativeContainer):
    admin_repository = providers.Singleton(AdminPostgresRepository, session=session_provider)
    subscription_repository = providers.Singleton(SubscriptionPostgresRepository, session=session_provider)
    gym_repository = providers.Singleton(GymPostgresRepository, session=session_provider)
    failed_domain_event_repository = providers.Singleton(FailedDomainEventTinyDBRepository)
