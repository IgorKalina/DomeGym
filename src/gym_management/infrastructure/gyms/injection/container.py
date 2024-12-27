from dependency_injector import containers, providers

from src.gym_management.application.gyms.commands.create_gym import CreateGym, CreateGymHandler
from src.shared_kernel.application.event.eventbus import EventBus


class GymContainer(containers.DeclarativeContainer):
    repositories = providers.DependenciesContainer()
    domain_eventbus = providers.Dependency(instance_of=EventBus)

    commands = providers.Dict(
        {
            CreateGym: providers.Factory(
                CreateGymHandler,
                subscriptions_repository=repositories.subscriptions_repository,
                eventbus=domain_eventbus,
            )
        }
    )
