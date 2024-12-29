import logging

from fastapi import FastAPI

from src.gym_management.infrastructure.common.config import load_config
from src.gym_management.presentation.api.api import init_api, run_api

logger = logging.getLogger(__name__)


# todo: replace this with a json logger
def setup_logger(level: int | str = logging.INFO) -> None:
    logging.basicConfig(
        level=level,
        format="%(asctime)s: [%(name)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def create_app() -> FastAPI:
    config = load_config()
    setup_logger(config.logger.level)
    return init_api(config.api)


if __name__ == "__main__":
    config = load_config()
    run_api(app="main:create_app", factory=True, config=config.uvicorn)
