import logging

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


def init_api(
    config: ApiConfig,
) -> FastAPI:
    logger.debug("Initialize API")
    app = FastAPI(
        debug=config.debug,
        title=config.title,
        version=config.version,
        default_response_class=ORJSONResponse,
    )
    setup_controllers(app)
    setup_middlewares(app)
    setup_dependency_injection(app)
    return app


def run_api(
    app: FastAPI | str,
    config: UvicornConfig,
) -> None:
    logger.info("Running API")
    uvicorn.run(app, host=config.host, port=config.port, log_level=config.log_level, reload=config.reload)
