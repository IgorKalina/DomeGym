from fastapi import FastAPI

from .v1.routes import router as gym_v1_router


def setup_gym_controllers(app: FastAPI) -> None:
    app.include_router(gym_v1_router)
