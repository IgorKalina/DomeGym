from typing import Awaitable, Callable

from dependency_injector.wiring import Provide
from fastapi import BackgroundTasks, Depends
from fastapi.requests import Request
from fastapi.responses import Response

from src.gym_management.infrastructure.common.injection.main import DiContainer
from src.shared_kernel.application.event.domain.event_bus import DomainEventBus


async def process_domain_events_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
    domain_event_bus: DomainEventBus = Depends(Provide[DiContainer.domain_event_bus]),
) -> Response:
    response = await call_next(request)
    background_tasks = BackgroundTasks()
    background_tasks.add_task(domain_event_bus.process_events)
    response.background = background_tasks
    return response
