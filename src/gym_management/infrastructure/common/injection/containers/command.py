from typing import Dict

from dependency_injector import containers, providers

from src.gym_management.application.gym.commands.create_gym import CreateGym, CreateGymHandler
from src.gym_management.application.gym.commands.remove_gym import RemoveGym, RemoveGymHandler
from src.gym_management.application.room.commands.create_room import CreateRoom, CreateRoomHandler
from src.gym_management.application.room.commands.remove_room import RemoveRoom, RemoveRoomHandler
from src.gym_management.application.subscription.commands.create_subscription import (
    CreateSubscription,
    CreateSubscriptionHandler,
)
from src.gym_management.application.subscription.commands.remove_subscription import (
    RemoveSubscription,
    RemoveSubscriptionHandler,
)
from src.gym_management.infrastructure.common.injection.containers.repository.base import RepositoryContainer
from src.shared_kernel.application.command import CommandBus
from src.shared_kernel.application.event.domain.event_bus import DomainEventBus
from src.shared_kernel.infrastructure.command.command_bus_memory import CommandBusMemory
from src.shared_kernel.infrastructure.interfaces.unit_of_work import UnitOfWork


async def _create_command_bus(unit_of_work: UnitOfWork, commands: Dict) -> CommandBusMemory:
    command_bus = CommandBusMemory(unit_of_work=unit_of_work)
    for command, handler in commands.items():
        command_bus.register_command_handler(command, handler)
    return command_bus


class CommandContainer(containers.DeclarativeContainer):
    repository_container: RepositoryContainer = providers.DependenciesContainer()
    domain_event_bus: DomainEventBus = providers.Dependency(instance_of=DomainEventBus)

    # Subscription
    create_subscription_handler = providers.Factory(
        CreateSubscriptionHandler,
        admin_repository=repository_container.admin_repository,
        domain_event_repository=repository_container.domain_event_repository,
    )
    remove_subscription_handler = providers.Factory(
        RemoveSubscriptionHandler,
        admin_repository=repository_container.admin_repository,
        subscription_repository=repository_container.subscription_repository,
        domain_event_repository=repository_container.domain_event_repository,
    )

    # Gym
    create_gym_handler = providers.Factory(
        CreateGymHandler,
        subscription_repository=repository_container.subscription_repository,
        domain_event_repository=repository_container.domain_event_repository,
    )
    remove_gym_handler = providers.Factory(
        RemoveGymHandler,
        gym_repository=repository_container.gym_repository,
        subscription_repository=repository_container.subscription_repository,
        domain_event_repository=repository_container.domain_event_repository,
    )

    # Room
    create_room_handler = providers.Factory(
        CreateRoomHandler,
        subscription_repository=repository_container.subscription_repository,
        gym_repository=repository_container.gym_repository,
        domain_event_repository=repository_container.domain_event_repository,
    )
    remove_room_handler = providers.Factory(
        RemoveRoomHandler,
        room_repository=repository_container.room_repository,
        gym_repository=repository_container.gym_repository,
        domain_event_repository=repository_container.domain_event_repository,
    )

    commands = providers.Dict(
        {
            # Subscription
            CreateSubscription: create_subscription_handler,
            RemoveSubscription: remove_subscription_handler,
            # Gym
            CreateGym: create_gym_handler,
            RemoveGym: remove_gym_handler,
            # Room
            CreateRoom: create_room_handler,
            RemoveRoom: remove_room_handler,
        },
    )

    command_bus: providers.Factory[CommandBus] = providers.Factory(
        _create_command_bus,
        unit_of_work=repository_container.unit_of_work,
        commands=commands,
    )
