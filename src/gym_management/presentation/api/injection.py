from fastapi import FastAPI

from src.gym_management import presentation
from src.gym_management.infrastructure.subscriptions.injection.main import SubscriptionsContainer


def setup_dependency_injection(app: FastAPI) -> None:
    subscription_commands_container = SubscriptionsContainer()
    subscription_commands_container.wire(packages=[presentation])
    app.container = subscription_commands_container
