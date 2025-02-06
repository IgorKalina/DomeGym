import asyncio
import logging
from typing import AsyncGenerator, Generator

import pytest
from alembic.command import upgrade
from alembic.config import Config as AlembicConfig
from docker import DockerClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from testcontainers.postgres import PostgresContainer
from testcontainers.rabbitmq import RabbitMqContainer

from src.gym_management.infrastructure.injection.containers.eventbus.rabbitmq import EventbusRabbitmqContainer

# from testcontainers.rabbitmq import RabbitMqContainer
from src.gym_management.infrastructure.injection.containers.repository.postgres import (
    RepositoryPostgresContainer,
)
from src.gym_management.infrastructure.injection.main import DiContainer
from src.gym_management.infrastructure.postgres.models.base_model import BaseModel
from tests.common.gym_management.common.config.config import ConfigTest
from tests.common.gym_management.common.config.mappers import map_database_full_url_to_config

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def config() -> ConfigTest:
    return ConfigTest()


def _remove_running_container_if_exists(docker_client: DockerClient, host_port: int) -> None:
    for container in docker_client.containers.list():
        port_mappings = container.attrs["NetworkSettings"]["Ports"] or {}
        for port_mapping, port_configs in port_mappings.items():
            if port_configs is None:
                continue
            for config in port_configs:
                if config.get("HostPort") == str(host_port):
                    logger.info(f"Stopping container {container.id} using port {host_port}...")
                    container.stop()
                    container.remove(v=True)


# Postgres
@pytest.fixture(scope="session", autouse=True)
def postgres(config: ConfigTest) -> Generator[PostgresContainer, None, None]:
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
        yield postgres
    finally:
        if postgres.get_wrapped_container() is not None:
            postgres.stop()


@pytest.fixture(scope="session")
def postgres_url(postgres: PostgresContainer) -> str:
    return postgres.get_connection_url().replace("psycopg2", "asyncpg")


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


# RabbitMQ
@pytest.fixture(scope="session", autouse=True)
def rabbitmq(config: ConfigTest) -> Generator[RabbitMqContainer, None, None]:
    rabbitmq = RabbitMqContainer(
        "rabbitmq:4.0.5-management-alpine",
        username=config.database.user.name,
        password=config.rabbitmq.user.password.get_secret_value(),
        port=config.rabbitmq.port,
    )
    _remove_running_container_if_exists(
        docker_client=rabbitmq.get_docker_client().client, host_port=config.rabbitmq.port
    )
    rabbitmq.with_bind_ports(container=rabbitmq.RABBITMQ_NODE_PORT, host=config.rabbitmq.port)
    try:
        rabbitmq.start()
        yield rabbitmq
    finally:
        if rabbitmq.get_wrapped_container() is not None:
            rabbitmq.stop()


@pytest.fixture
async def di_container(postgres_url: str, config: ConfigTest) -> AsyncGenerator[DiContainer, None]:  # noqa: ARG001
    database_config = map_database_full_url_to_config(postgres_url)
    repository_container = RepositoryPostgresContainer(config=database_config)
    eventbus_container = EventbusRabbitmqContainer(config=config.rabbitmq)
    di_container = DiContainer(
        repository_container=repository_container,
        eventbus_container=eventbus_container,
    )
    di_container.background_task_scheduler.override(lambda: None)
    await di_container.init_resources()

    yield di_container

    session: AsyncSession = await repository_container.session_provider()
    await _truncate_all_tables(session)
    await di_container.shutdown_resources()
