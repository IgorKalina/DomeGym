import logging

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


def start_api() -> None:
    config = load_config()
    setup_logger(config.logger.level)
    api = init_api(config.api)
    run_api(app=api, config=config.uvicorn)


if __name__ == "__main__":
    start_api()
