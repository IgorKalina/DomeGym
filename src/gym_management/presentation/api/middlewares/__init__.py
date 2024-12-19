from typing import Awaitable, Callable

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware


async def dummy_dispatcher(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    return await call_next(request)


def setup_middlewares(app: FastAPI) -> None:
    app.add_middleware(BaseHTTPMiddleware, dispatch=dummy_dispatcher)
