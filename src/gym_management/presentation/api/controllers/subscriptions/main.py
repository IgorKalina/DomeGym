from fastapi import FastAPI

from .v1.routes import router as subscription_v1_router


def setup_subscription_controllers(app: FastAPI) -> None:
    app.include_router(subscription_v1_router)
