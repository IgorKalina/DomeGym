import asyncio
import logging
import typing
from typing import AsyncGenerator, Generator

import pytest
from alembic.command import upgrade
from alembic.config import Config as AlembicConfig
from docker import DockerClient
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
from src.gym_management.presentation.api.controllers.gym.v1.responses.gym_response import GymResponse
from src.gym_management.presentation.api.controllers.room.v1.responses.room_response import RoomResponse
from src.gym_management.presentation.api.controllers.subscription.v1.responses.subscription_response import (
    SubscriptionResponse,
)
from tests.common.gym_management.common.config.config import ConfigTest
from tests.common.gym_management.common.config.mappers import map_database_full_url_to_config
from tests.common.gym_management.gym.factory.gym_request_factory import GymRequestFactory
from tests.common.gym_management.gym.service.api.v1 import GymV1ApiService
from tests.common.gym_management.room.factory.room_request_factory import RoomRequestFactory
from tests.common.gym_management.room.service.api.v1 import RoomV1ApiService
from tests.common.gym_management.subscription.factory.subscription_request_factory import SubscriptionRequestFactory
from tests.common.gym_management.subscription.service.api.v1 import SubscriptionV1ApiService

if typing.TYPE_CHECKING:
    from src.gym_management.presentation.api.controllers.gym.v1.requests.create_gym_request import CreateGymRequest
    from src.gym_management.presentation.api.controllers.room.v1.requests.create_gym_request import CreateRoomRequest
    from src.gym_management.presentation.api.controllers.subscription.v1.requests.create_subscription_request import (
        CreateSubscriptionRequest,
    )


logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def config() -> ConfigTest:
    return ConfigTest()


def _remove_running_container_if_exists(docker_client: DockerClient, host_port: int) -> None:
    for container in docker_client.containers.list():
        port_mappings = container.attrs["NetworkSettings"]["Ports"]
        if port_mappings and any(p[0]["HostPort"] == str(host_port) for p in port_mappings.values()):
            logger.info(f"Stopping container {container.id} using port {host_port}...")
            container.stop()
            container.remove()


@pytest.fixture(scope="session")
def postgres_url(config: ConfigTest) -> Generator[str, None, None]:
    postgres = PostgresContainer(
        "postgres:16-alpine",
        dbname=config.database.name,
        user=config.database.user.name,
        password=config.database.user.password.get_secret_value(),
    )
    _remove_running_container_if_exists(
        docker_client=postgres.get_docker_client().client, host_port=config.database.port
    )
    postgres.with_bind_ports(container=postgres.port_to_expose, host=config.database.port)
    try:
        postgres.start()
        postgres_url = postgres.get_connection_url().replace("psycopg2", "asyncpg")
        yield postgres_url
    finally:
        if postgres.get_wrapped_container() is not None:
            postgres.stop()


@pytest.fixture(scope="session", autouse=True)
async def _apply_db_migrations(postgres_url: str, config: ConfigTest) -> None:  # noqa: ARG001
    alembic_config = AlembicConfig("alembic.ini")
    alembic_config.set_main_option("sqlalchemy.url", config.database.full_url)
    await asyncio.to_thread(upgrade, alembic_config, "head")


async def _truncate_all_tables(session: AsyncSession) -> None:
    """
    Truncates all tables associated with subclasses of BaseModel using an AsyncSession.
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
async def di_container(postgres_url: str) -> AsyncGenerator[DiContainer, None]:  # noqa: ARG001
    database_config = map_database_full_url_to_config(postgres_url)
    repository_container = RepositoryPostgresContainer(config=database_config)
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


@pytest.fixture
def room_v1_api(api_client: AsyncClient) -> RoomV1ApiService:
    return RoomV1ApiService(api_client)


@pytest.fixture
async def subscription_v1(subscription_v1_api: SubscriptionV1ApiService) -> SubscriptionResponse:
    request: CreateSubscriptionRequest = SubscriptionRequestFactory.create_create_subscription_request()
    _, response_data = await subscription_v1_api.create(request)
    return response_data.data[0]


@pytest.fixture
async def gym_v1(subscription_v1: SubscriptionResponse, gym_v1_api: GymV1ApiService) -> GymResponse:
    request: CreateGymRequest = GymRequestFactory.create_create_gym_request()
    _, response_data = await gym_v1_api.create(request=request, subscription_id=subscription_v1.id)
    return response_data.data[0]


@pytest.fixture
async def room_v1(gym_v1: GymResponse, room_v1_api: RoomV1ApiService) -> RoomResponse:
    request: CreateRoomRequest = RoomRequestFactory.create_create_room_request()
    _, response_data = await room_v1_api.create(
        request=request,
        gym_id=gym_v1.id,
        subscription_id=gym_v1.subscription_id,
    )
    return response_data.data[0]
