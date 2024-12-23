from typing import List

from dependency_injector import containers, providers

from src.gym_management.infrastructure.common.injection.containers.repository import RepositoryContainer
from src.gym_management.infrastructure.gyms.injection.container import GymContainer
from src.gym_management.infrastructure.subscriptions.injection.container import SubscriptionsContainer
from src.shared_kernel.infrastructure.command.command_invoker_memory import CommandInvokerMemory
from src.shared_kernel.infrastructure.query.query_invoker_memory import QueryInvokerMemory


def register_commands(
    command_invoker: CommandInvokerMemory, containers: List[containers.DeclarativeContainer]
) -> CommandInvokerMemory:
    for container in containers:
        if not hasattr(container, "commands"):
            continue
        for command, handler in container.commands().items():
            command_invoker.register_command_handler(command, handler)
    return command_invoker


def register_queries(
    query_invoker: QueryInvokerMemory, containers: List[containers.DeclarativeContainer]
) -> QueryInvokerMemory:
    for container in containers:
        if not hasattr(container, "queries"):
            continue
        for command, handler in container.queries().items():
            query_invoker.register_query_handler(command, handler)
    return query_invoker


class DiContainer(containers.DeclarativeContainer):
    repositories = providers.Container(RepositoryContainer)
    __containers = [
        providers.Container(SubscriptionsContainer, repositories=repositories),
        providers.Container(GymContainer, repositories=repositories),
    ]

    command_invoker = providers.Resource(
        register_commands,
        command_invoker=providers.Singleton(CommandInvokerMemory),
        containers=__containers,
    )

    query_invoker = providers.Resource(
        register_queries,
        query_invoker=providers.Singleton(QueryInvokerMemory),
        containers=__containers,
    )
