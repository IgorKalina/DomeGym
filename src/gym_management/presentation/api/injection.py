from fastapi import FastAPI

from src.gym_management import presentation
from src.gym_management.infrastructure.common.injection.main import DiContainer


def setup_dependency_injection(app: FastAPI) -> DiContainer:
    di_container = DiContainer()
    di_container.wire(packages=[presentation])
    app.container = di_container
    return di_container
