import functools
from typing import Any, Awaitable, Callable, Dict

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dependency_injector import containers, providers

from src.gym_management.infrastructure.common.injection.containers.background_task import BackgroundTaskContainer
from src.gym_management.infrastructure.common.injection.containers.command import CommandContainer
from src.gym_management.infrastructure.common.injection.containers.domain_event import DomainEventContainer
from src.gym_management.infrastructure.common.injection.containers.eventbus.base import EventbusContainer
from src.gym_management.infrastructure.common.injection.containers.query import QueryContainer
from src.gym_management.infrastructure.common.injection.containers.repository.base import RepositoryContainer
from src.shared_kernel.infrastructure.command.command_bus_memory import CommandBusMemory
from src.shared_kernel.infrastructure.eventbus.eventbus_memory import DomainEventBusMemory
from src.shared_kernel.infrastructure.query.query_bus_memory import QueryBusMemory


async def register_commands(command_bus: CommandBusMemory, commands: Dict) -> CommandBusMemory:
    for command, handler in commands.items():
        command_bus.register_command_handler(command, handler)
    return command_bus


async def register_queries(query_bus: QueryBusMemory, queries: Dict) -> QueryBusMemory:
    for query, handler in queries.items():
        query_bus.register_query_handler(query, handler)
    return query_bus


async def register_domain_events(domain_event_bus: DomainEventBusMemory, domain_events: Dict) -> DomainEventBusMemory:
    for event, handlers in domain_events.items():
        for handler in handlers:
            await domain_event_bus.subscribe(event, handler)
    return domain_event_bus


def init_background_task_scheduler(background_tasks: BackgroundTaskContainer) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()

    def async_wrap(func: Callable[[], Awaitable[Any]]) -> Callable[[], Awaitable[Any]]:
        @functools.wraps(func)
        async def wrapped() -> Any:
            return await func()

        return wrapped

    scheduler.add_job(async_wrap(background_tasks.publish_domain_events), trigger="interval", seconds=10)
    try:
        scheduler.start()
        yield scheduler
    finally:
        scheduler.shutdown()


class DiContainer(containers.DeclarativeContainer):
    # dependencies
    repository_container: RepositoryContainer = providers.DependenciesContainer()
    eventbus_container: EventbusContainer = providers.DependenciesContainer()

    domain_event_bus = providers.Singleton(
        DomainEventBusMemory,
        event_repository=repository_container.failed_domain_event_repository,
    )
    query_bus = providers.Singleton(QueryBusMemory)
    command_bus = providers.Singleton(CommandBusMemory)

    # containers
    query_container = providers.Container(
        QueryContainer,
        query_bus=query_bus,
        repository_container=repository_container,
    )
    command_container = providers.Container(
        CommandContainer,
        query_bus=query_bus,
        repository_container=repository_container,
        domain_event_bus=domain_event_bus,
    )

    domain_event_container = providers.Container(
        DomainEventContainer,
        repository_container=repository_container,
        domain_event_bus=domain_event_bus,
    )

    background_tasks = providers.Container(
        BackgroundTaskContainer, repository_container=repository_container, eventbus_container=eventbus_container
    )

    _register_commands = providers.Resource(
        register_commands,
        command_bus=command_bus,
        commands=command_container.commands,
    )

    _register_queries = providers.Resource(
        register_queries,
        query_bus=query_bus,
        queries=query_container.queries,
    )

    _register_domain_events = providers.Resource(
        register_domain_events, domain_event_bus=domain_event_bus, domain_events=domain_event_container.domain_events
    )

    background_task_scheduler = providers.Resource(
        init_background_task_scheduler,
        background_tasks=background_tasks,
    )
