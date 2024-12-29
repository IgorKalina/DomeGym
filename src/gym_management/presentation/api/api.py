import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import (
    FastAPI,
)
from fastapi.responses import (
    ORJSONResponse,
)

from src.gym_management.infrastructure.common.config.api import ApiConfig, UvicornConfig
from src.gym_management.presentation.api.controllers.main import setup_controllers
from src.gym_management.presentation.api.injection import setup_dependency_injection
from src.gym_management.presentation.api.middlewares import setup_middlewares

logger = logging.getLogger(__name__)


@asynccontextmanager
async def api_lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    di_container = setup_dependency_injection(app)
    await di_container.init_resources()
    try:
        yield
    finally:
        await di_container.shutdown_resources()


def init_api(
    config: ApiConfig,
) -> FastAPI:
    logger.debug("Initialize API")
    app = FastAPI(
        debug=config.debug,
        title=config.title,
        version=config.version,
        default_response_class=ORJSONResponse,
        lifespan=api_lifespan,
    )
    setup_dependency_injection(app)
    setup_controllers(app)
    setup_middlewares(app)
    return app


def run_api(
    app: FastAPI | str,
    factory: bool,
    config: UvicornConfig,
) -> None:
    logger.info("Running API")
    uvicorn.run(
        app, factory=factory, host=config.host, port=config.port, log_level=config.log_level, reload=config.reload
    )
