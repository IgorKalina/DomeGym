from typing import List

from dependency_injector import containers, providers

from src.gym_management.infrastructure.common.injection.containers.repository import RepositoryContainer
from src.gym_management.infrastructure.gyms.injection.container import GymContainer
from src.gym_management.infrastructure.subscriptions.injection.container import SubscriptionsContainer
from src.shared_kernel.application.command import CommandInvoker
from src.shared_kernel.application.command.command_invoker_memory import CommandInvokerMemory


def register_commands(
    command_invoker: CommandInvoker, containers: List[containers.DeclarativeContainer]
) -> CommandInvoker:
    for container in containers:
        if not hasattr(container, "commands"):
            continue
        for command, handler in container.commands().items():
            command_invoker.register_command_handler(command, handler)
    return command_invoker


class DiContainer(containers.DeclarativeContainer):
    repositories = providers.Container(RepositoryContainer)

    command_invoker = providers.Resource(
        register_commands,
        command_invoker=providers.Singleton(CommandInvokerMemory),
        containers=[
            providers.Container(SubscriptionsContainer, repositories=repositories),
            providers.Container(GymContainer, repositories=repositories),
        ],
    )
