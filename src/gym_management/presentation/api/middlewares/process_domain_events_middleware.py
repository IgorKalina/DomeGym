import logging
from typing import TYPE_CHECKING, Awaitable, Callable

from dependency_injector.wiring import Provide, inject
from fastapi import BackgroundTasks, Depends
from fastapi.requests import Request
from fastapi.responses import Response

from src.gym_management.infrastructure.common.injection.containers.repository_postgres import (
    RepositoryPostgresContainer,
)
from src.gym_management.infrastructure.common.injection.main import DiContainer
from src.shared_kernel.application.event.domain.eventbus import DomainEventBus
from src.shared_kernel.application.exceptions import EventualConsistencyError

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


logger = logging.getLogger(__name__)


# async def process_domain_events_middleware(
#     request: Request,
#     call_next: Callable[[Request], Awaitable[Response]],
#     domain_eventbus: DomainEventBus = Depends(Provide[DiContainer.domain_eventbus]),
# ) -> Response:
#     response = await call_next(request)
#     background_tasks = BackgroundTasks()
#     background_tasks.add_task(domain_eventbus.process_events)
#     response.background = background_tasks
#     return response


@inject
async def process_domain_events_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
    domain_eventbus: DomainEventBus = Depends(Provide[DiContainer.domain_eventbus]),
    repository_container: RepositoryPostgresContainer = Depends(Provide[DiContainer.repository_container]),
) -> Response:
    logger.debug(f"Received an API request: {request.method} {request.url}")
    session: AsyncSession = await repository_container.session_provider()
    async with session.begin():
        logger.debug("Starting a new transaction to handle an incoming request")
        response = await call_next(request)
        try:
            background_tasks = BackgroundTasks()
            background_tasks.add_task(domain_eventbus.process_events)
            response.background = background_tasks
        except EventualConsistencyError:
            await session.rollback()
        else:
            await session.commit()
    logger.debug("Transaction closed")
    return response
