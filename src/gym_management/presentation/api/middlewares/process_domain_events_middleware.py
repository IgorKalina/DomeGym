import logging
from http import HTTPMethod
from typing import Awaitable, Callable

from fastapi import BackgroundTasks
from fastapi.requests import Request
from fastapi.responses import Response

from src.gym_management.infrastructure.common.background_services.domain_events.process_domain_events import (
    process_domain_events,
)

logger = logging.getLogger(__name__)


async def process_domain_events_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    response = await call_next(request)

    if request.method == HTTPMethod.GET:
        logger.debug("GET request. Domain events are not processed")
        return response

    background_tasks = BackgroundTasks()
    background_tasks.add_task(process_domain_events)
    response.background = background_tasks
    return response
