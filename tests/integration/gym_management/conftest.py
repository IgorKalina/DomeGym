import asyncio
import logging
from typing import AsyncGenerator, Generator

import pytest
from alembic.command import upgrade
from alembic.config import Config as AlembicConfig
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from testcontainers.postgres import PostgresContainer

from src.gym_management.infrastructure.common.config import load_config
from src.gym_management.infrastructure.common.injection.containers.repository_postgres import (
    RepositoryPostgresContainer,
)
from src.gym_management.infrastructure.common.injection.main import DiContainer
from src.gym_management.infrastructure.common.postgres.models.base_model import BaseModel
from src.gym_management.presentation.api.api import init_api
from tests.common.gym_management.config.config import ConfigTest
from tests.common.gym_management.gym.service.api_v1 import GymV1ApiService
from tests.common.gym_management.subscription.service.api_v1 import SubscriptionV1ApiService

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def config() -> ConfigTest:
    return ConfigTest()


@pytest.fixture(scope="session")
def postgres_container(config: ConfigTest) -> Generator[None, None, None]:
    postgres = PostgresContainer(
        "postgres:16-alpine",
        driver="psycopg2",
        dbname=config.database.name,
        user=config.database.user.name,
        password=config.database.user.password.get_secret_value(),
    )
    postgres.with_bind_ports(container=postgres.port_to_expose, host=config.database.port)
    try:
        postgres.start()
        yield
    finally:
        if postgres.get_wrapped_container() is not None:
            postgres.stop()


@pytest.fixture(scope="session", autouse=True)
async def _apply_db_migrations(postgres_container: None, config: ConfigTest) -> None:  # noqa: ARG001
    alembic_config = AlembicConfig("alembic.ini")
    alembic_config.set_main_option("sqlalchemy.url", config.database.full_url)
    await asyncio.to_thread(upgrade, alembic_config, "head")


async def _truncate_all_tables(session: AsyncSession) -> None:
    """
    Truncates all tables associated with subclasses of BaseModel using an AsyncSession.

    Args:
        session (AsyncSession): SQLAlchemy AsyncSession to interact with the database.
    """
    # Disable constraints to allow truncation of tables with foreign keys
    await session.execute(text("SET session_replication_role = 'replica';"))

    table_names = [table.name for table in BaseModel.metadata.sorted_tables]

    for table_name in table_names:
        await session.execute(text(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE;"))

    # Re-enable constraints
    await session.execute(text("SET session_replication_role = 'origin';"))
    await session.commit()


@pytest.fixture
async def di_container(postgres_container: None, config: ConfigTest) -> AsyncGenerator[DiContainer, None]:  # noqa: ARG001
    repository_container = RepositoryPostgresContainer(config=config)
    di_container = DiContainer(repository_container=repository_container)
    await di_container.init_resources()
    yield di_container
    session: AsyncSession = await repository_container.session_provider()
    await _truncate_all_tables(session)
    await di_container.shutdown_resources()


@pytest.fixture
async def api_client(di_container: DiContainer) -> AsyncClient:
    api = init_api(config=load_config().api)
    api.container.override(di_container)  # type: ignore
    async with AsyncClient(transport=ASGITransport(app=api), base_url="http://testserver") as async_client:
        yield async_client


@pytest.fixture
def subscription_v1_api(api_client: AsyncClient) -> SubscriptionV1ApiService:
    return SubscriptionV1ApiService(api_client)


@pytest.fixture
def gym_v1_api(api_client: AsyncClient) -> GymV1ApiService:
    return GymV1ApiService(api_client)
