import asyncio
import logging

from src.presentation.api.config import APIConfig
from src.presentation.api.main import init_api, run_api

logger = logging.getLogger(__name__)


def setup_logger(level=logging.INFO):
    logging.basicConfig(
        level=level,
        format="%(asctime)s: [%(name)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


async def run_app():
    api = init_api()
    await run_api(app=api, api_config=APIConfig())


if __name__ == "__main__":
    setup_logger()
    asyncio.run(run_app())
