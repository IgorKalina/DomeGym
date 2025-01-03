from dependency_injector import containers, providers

from src.gym_management.application.gym.commands.create_gym import CreateGym, CreateGymHandler
from src.gym_management.application.gym.queries.get_gym import GetGym, GetGymHandler
from src.shared_kernel.application.event.domain.eventbus import DomainEventBus


class GymContainer(containers.DeclarativeContainer):
    repositories = providers.DependenciesContainer()
    domain_eventbus = providers.Dependency(instance_of=DomainEventBus)

    commands = providers.Dict(
        {
            CreateGym: providers.Factory(
                CreateGymHandler,
                subscription_repository=repositories.subscription_repository,
                gym_repository=repositories.gym_repository,
                eventbus=domain_eventbus,
            )
        }
    )
    queries = providers.Dict(
        {
            GetGym: providers.Factory(
                GetGymHandler,
                subscription_repository=repositories.subscription_repository,
                gym_repository=repositories.gym_repository,
            ),
        }
    )
