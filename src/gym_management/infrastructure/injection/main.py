import functools
from typing import Any, Awaitable, Callable, Dict

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dependency_injector import containers, providers

from src.gym_management.infrastructure.injection.containers.background_task import BackgroundTaskContainer
from src.gym_management.infrastructure.injection.containers.command import CommandContainer
from src.gym_management.infrastructure.injection.containers.domain_event import DomainEventContainer
from src.gym_management.infrastructure.injection.containers.eventbus.base import EventbusContainer
from src.gym_management.infrastructure.injection.containers.query import QueryContainer
from src.gym_management.infrastructure.injection.containers.repository.base import RepositoryContainer
from src.shared_kernel.infrastructure.command.command_invoker_memory import CommandInvokerMemory
from src.shared_kernel.infrastructure.eventbus.eventbus_memory import DomainEventBusMemory
from src.shared_kernel.infrastructure.query.query_invoker_memory import QueryInvokerMemory


async def register_commands(command_invoker: CommandInvokerMemory, commands: Dict) -> CommandInvokerMemory:
    for command, handler in commands.items():
        command_invoker.register_command_handler(command, handler)
    return command_invoker


async def register_queries(query_invoker: QueryInvokerMemory, queries: Dict) -> QueryInvokerMemory:
    for query, handler in queries.items():
        query_invoker.register_query_handler(query, handler)
    return query_invoker


async def register_domain_events(domain_eventbus: DomainEventBusMemory, domain_events: Dict) -> DomainEventBusMemory:
    for event, handlers in domain_events.items():
        for handler in handlers:
            await domain_eventbus.subscribe(event, handler)
    return domain_eventbus


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

    domain_eventbus = providers.Singleton(
        DomainEventBusMemory,
        event_repository=repository_container.failed_domain_event_repository,
    )
    # containers
    command_container = providers.Container(
        CommandContainer, repository_container=repository_container, domain_eventbus=domain_eventbus
    )
    query_container = providers.Container(
        QueryContainer, repository_container=repository_container, domain_eventbus=domain_eventbus
    )
    domain_event_container = providers.Container(
        DomainEventContainer, repository_container=repository_container, domain_eventbus=domain_eventbus
    )

    background_tasks = providers.Container(
        BackgroundTaskContainer, repository_container=repository_container, eventbus_container=eventbus_container
    )

    command_invoker = providers.Resource(
        register_commands,
        command_invoker=providers.Singleton(CommandInvokerMemory),
        commands=command_container.commands,
    )

    query_invoker = providers.Resource(
        register_queries,
        query_invoker=providers.Singleton(QueryInvokerMemory),
        queries=query_container.queries,
    )

    domain_eventbus = providers.Resource(
        register_domain_events, domain_eventbus=domain_eventbus, domain_events=domain_event_container.domain_events
    )

    background_task_scheduler = providers.Resource(
        init_background_task_scheduler,
        background_tasks=background_tasks,
    )
