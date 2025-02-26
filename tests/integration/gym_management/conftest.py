import logging
from typing import AsyncGenerator

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.gym_management.infrastructure.common.injection.main import DiContainer
from src.gym_management.infrastructure.common.postgres.models.base_model import BaseModel
from tests.common.gym_management.common.config.config import ConfigTest

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def config() -> ConfigTest:
    return ConfigTest()


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
async def di_container(config: ConfigTest) -> AsyncGenerator[DiContainer, None]:  # noqa: ARG001
    di_container = DiContainer()
    di_container.config.override(config)
    await di_container.init_resources()

    yield di_container

    session: AsyncSession = await di_container.repository_container.session()
    await _truncate_all_tables(session)
    await di_container.shutdown_resources()
