import logging

import uvicorn
from fastapi import (
    FastAPI,
)
from fastapi.responses import (
    ORJSONResponse,
)

from src.gym_management.infrastructure.common.config.api import ApiConfig, UvicornConfig

logger = logging.getLogger(__name__)


def init_api(
    config: ApiConfig,
) -> FastAPI:
    logger.debug("Initialize API")
    return FastAPI(
        debug=config.debug,
        title=config.title,
        version=config.version,
        default_response_class=ORJSONResponse,
    )


def run_api(
    app: FastAPI,
    config: UvicornConfig,
) -> None:
    logger.info("Running API")
    uvicorn.run(app, host=config.host, port=config.port, log_level=config.log_level)
