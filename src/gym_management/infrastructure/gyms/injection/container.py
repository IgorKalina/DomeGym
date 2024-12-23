from dependency_injector import containers, providers

from src.gym_management.application.gyms.commands.create_gym import CreateGym, CreateGymHandler


class GymContainer(containers.DeclarativeContainer):
    repositories = providers.DependenciesContainer()

    commands = providers.Dict(
        {
            CreateGym: providers.Factory(
                CreateGymHandler,
                subscriptions_repository=repositories.subscriptions_repository,
            )
        }
    )
