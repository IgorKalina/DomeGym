import asyncio
from typing import Awaitable, Callable

from dependency_injector.wiring import Provide
from fastapi import Depends
from fastapi.requests import Request
from fastapi.responses import Response

from src.gym_management.infrastructure.common.injection.main import DiContainer
from src.shared_kernel.application.event.eventbus import EventBus


async def process_domain_events_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
    domain_eventbus: EventBus = Depends(Provide[DiContainer.domain_eventbus]),
) -> Response:
    response = await call_next(request)
    asyncio.create_task(domain_eventbus.process_events())
    return response
