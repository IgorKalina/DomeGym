from src.gym_management import presentation
from src.gym_management.infrastructure.common import background_services
from src.gym_management.infrastructure.common.config import load_config
from src.gym_management.infrastructure.common.injection.main import DiContainer


def create_dependency_injection_container() -> DiContainer:
    config = load_config()
    di_container = DiContainer(config=config)
    di_container.wire(packages=[presentation, background_services])
    return di_container
