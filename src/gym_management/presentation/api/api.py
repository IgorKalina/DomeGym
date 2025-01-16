import asyncio
import logging
from contextlib import asynccontextmanager
from typing import AsyncContextManager, AsyncGenerator, Callable

import uvicorn
from fastapi import (
    FastAPI,
)
from fastapi.responses import (
    ORJSONResponse,
)

from src.gym_management.infrastructure.common.config.api import ApiConfig, UvicornConfig
from src.gym_management.infrastructure.common.injection.main import DiContainer
from src.gym_management.presentation.api.controllers.main import setup_controllers
from src.gym_management.presentation.api.injection import create_dependency_injection_container
from src.shared_kernel.infrastructure.event.domain.functions import reprocess_failed_domain_events

logger = logging.getLogger(__name__)


def api_lifespan(di_container: DiContainer) -> Callable[[FastAPI], AsyncContextManager[None]]:
    @asynccontextmanager
    async def _lifespan(app: FastAPI) -> AsyncGenerator[None, None]:  # noqa: ARG001
        await di_container.init_resources()
        asyncio.create_task(
            reprocess_failed_domain_events(
                failed_events_repository=di_container.repository_container.failed_domain_event_repository(),
                domain_eventbus=await di_container.domain_eventbus(),
            )
        )
        try:
            yield
        finally:
            await di_container.shutdown_resources()

    return _lifespan


def init_api(
    config: ApiConfig,
) -> FastAPI:
    logger.debug("Initialize API")
    di_container = create_dependency_injection_container()
    app = FastAPI(
        debug=config.debug,
        title=config.title,
        version=config.version,
        default_response_class=ORJSONResponse,
        lifespan=api_lifespan(di_container),
    )
    setup_controllers(app)
    # setup_middlewares(app)
    app.container = di_container
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
