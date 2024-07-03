from typing import Awaitable, Callable
from uuid import uuid4

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware


async def dummy_dispatcher(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    response = await call_next(request)
    return response


def setup_middlewares(app: FastAPI):
    app.add_middleware(BaseHTTPMiddleware, dispatch=dummy_dispatcher)
