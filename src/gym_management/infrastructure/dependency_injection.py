from typing import AsyncGenerator

import orjson
from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from src.gym_management.common.settings.config import settings
from src.gym_management.infrastructure.admins.repositories.memory_repository import AdminsMemoryRepository
from src.gym_management.infrastructure.db.repositories.subscriptions_repository import SubscriptionsPostgresRepository


async def build_sa_engine() -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(
        url=settings.database.full_url,
        echo=True,
        echo_pool=True,
        json_serializer=lambda data: orjson.dumps(data).decode(),
        json_deserializer=orjson.loads,
        pool_size=50,
    )
    yield engine

    await engine.dispose()


def build_sa_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    session_factory = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    return session_factory


async def build_sa_session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session


async def init_postgres_session() -> AsyncSession:
    engine = create_async_engine(
        url=settings.database.full_url,
        echo=True,
        echo_pool=True,
        json_serializer=lambda data: orjson.dumps(data).decode(),
        json_deserializer=orjson.loads,
        pool_size=50,
    )
    session_factory = build_sa_session_factory(engine)
    async with session_factory() as session:
        yield session

    await engine.dispose()


class InfrastructureContainer(containers.DeclarativeContainer):
    _postgres_session = providers.Resource(init_postgres_session)
    admins_repository = providers.Singleton(AdminsMemoryRepository)
    subscriptions_repository = providers.Singleton(SubscriptionsPostgresRepository, session=_postgres_session)
