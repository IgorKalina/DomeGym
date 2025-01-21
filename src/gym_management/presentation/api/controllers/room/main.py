from fastapi import FastAPI

from .v1.routes import router as room_v1_router


def setup_room_controllers(app: FastAPI) -> None:
    app.include_router(room_v1_router)
