from fastapi import FastAPI

from .exceptions import setup_exception_handlers
from .gyms.main import setup_gym_controllers
from .subscriptions.main import setup_subscription_controllers


def setup_controllers(app: FastAPI) -> None:
    setup_gym_controllers(app)
    setup_subscription_controllers(app)
    setup_exception_handlers(app)
