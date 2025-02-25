from typing import Awaitable, Callable

from fastapi import BackgroundTasks
from fastapi.requests import Request
from fastapi.responses import Response

from src.gym_management.infrastructure.common.background_services.domain_events.process_domain_events import (
    process_domain_events,
)


async def process_domain_events_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    response = await call_next(request)
    background_tasks = BackgroundTasks()
    background_tasks.add_task(process_domain_events)
    response.background = background_tasks
    return response
