from typing import Dict

from dependency_injector import containers, providers

from src.gym_management.infrastructure.common.injection.containers.command import CommandContainer
from src.gym_management.infrastructure.common.injection.containers.domain_event import DomainEventContainer
from src.gym_management.infrastructure.common.injection.containers.query import QueryContainer
from src.gym_management.infrastructure.common.injection.containers.repository_base import RepositoryContainer
from src.shared_kernel.infrastructure.command.command_invoker_memory import CommandInvokerMemory
from src.shared_kernel.infrastructure.event.domain.eventbus_memory import DomainEventBusMemory
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


class DiContainer(containers.DeclarativeContainer):
    repository = providers.Container(RepositoryContainer)

    __domain_eventbus = providers.Singleton(
        DomainEventBusMemory,
        event_repository=repository.failed_domain_event_repository,
    )
    __command_container = providers.Container(
        CommandContainer, repository=repository, domain_eventbus=__domain_eventbus
    )
    __query_container = providers.Container(QueryContainer, repository=repository, domain_eventbus=__domain_eventbus)
    __domain_event_container = providers.Container(
        DomainEventContainer, repository=repository, domain_eventbus=__domain_eventbus
    )

    command_invoker = providers.Resource(
        register_commands,
        command_invoker=providers.Singleton(CommandInvokerMemory),
        commands=__command_container.commands,
    )

    query_invoker = providers.Resource(
        register_queries,
        query_invoker=providers.Singleton(QueryInvokerMemory),
        queries=__query_container.queries,
    )

    domain_eventbus = providers.Resource(
        register_domain_events, domain_eventbus=__domain_eventbus, domain_events=__domain_event_container.domain_events
    )
