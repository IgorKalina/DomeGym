import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.gym_management import presentation

from .config import APIConfig
from .controllers.main import setup_controllers
from .dependency_injection import DependencyContainer

logger = logging.getLogger(__name__)


def init_api(debug: bool = True) -> FastAPI:
    logger.debug("Initialize API")
    app = FastAPI(
        debug=debug,
        title="Gym Management",
        version="1.0.0",
        default_response_class=ORJSONResponse,
    )
    container = DependencyContainer()
    container.wire(packages=[presentation])
    app.container = container
    setup_controllers(app)
    return app


async def run_api(app: FastAPI, api_config: APIConfig) -> None:
    config = uvicorn.Config(
        app,
        host=api_config.host,
        port=api_config.port,
        log_level=logging.DEBUG,
        log_config=None,
    )
    server = uvicorn.Server(config)
    logger.info("Running API")
    await server.serve()
