import time
from typing import Never

from apscheduler.schedulers.background import BackgroundScheduler
from tenacity import retry, stop_after_attempt, wait_fixed

from src.gym_management import presentation
from src.gym_management.infrastructure.config import load_config
from src.gym_management.infrastructure.injection.containers.repository_postgres import (
    RepositoryPostgresContainer,
)
from src.gym_management.infrastructure.injection.main import DiContainer


def create_dependency_injection_container() -> DiContainer:
    repository_container = RepositoryPostgresContainer(config=load_config().database)
    di_container = DiContainer(repository_container=repository_container)
    di_container.wire(packages=[presentation])
    return di_container


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1), retry_error_cls=RuntimeError)
def gagarin() -> Never:
    raise RuntimeError()


if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(gagarin, trigger="interval", seconds=10)
    scheduler.start()
    time.sleep(500)
