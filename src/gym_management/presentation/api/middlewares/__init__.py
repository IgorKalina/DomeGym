from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from src.gym_management.presentation.api.middlewares.process_domain_events_middleware import (
    process_domain_events_middleware,
)


def setup_middlewares(app: FastAPI) -> None:
    app.add_middleware(BaseHTTPMiddleware, dispatch=process_domain_events_middleware)
