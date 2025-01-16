from fastapi import FastAPI

from .default import default_router
from .exceptions import setup_exception_handlers
from .gym.main import setup_gym_controllers
from .healthcheck import healthcheck_router
from .subscription.main import setup_subscription_controllers


def setup_controllers(app: FastAPI) -> None:
    app.include_router(default_router)
    app.include_router(healthcheck_router)
    setup_gym_controllers(app)
    setup_subscription_controllers(app)
    setup_exception_handlers(app)
