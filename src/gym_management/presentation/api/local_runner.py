import logging

from src.gym_management.presentation.api.main import init_api

logger = logging.getLogger(__name__)


def setup_logger(level=logging.INFO):
    logging.basicConfig(
        level=level,
        format="%(asctime)s: [%(name)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


setup_logger()
app = init_api()
