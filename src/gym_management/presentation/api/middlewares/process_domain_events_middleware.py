from typing import Awaitable, Callable

from dependency_injector.wiring import Provide
from fastapi import BackgroundTasks, Depends
from fastapi.requests import Request
from fastapi.responses import Response

from src.gym_management.infrastructure.injection.main import DiContainer
from src.shared_kernel.application.event.domain.eventbus import DomainEventBus


async def process_domain_events_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
    domain_eventbus: DomainEventBus = Depends(Provide[DiContainer.domain_eventbus]),
) -> Response:
    response = await call_next(request)
    background_tasks = BackgroundTasks()
    background_tasks.add_task(domain_eventbus.process_events)
    response.background = background_tasks
    return response
