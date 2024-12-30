from dependency_injector import containers, providers

from src.gym_management.application.room.domain_events.gym_added_handler import GymAddedEventHandler
from src.gym_management.domain.subscription.events.gym_added_event import GymAddedEvent


class RoomContainer(containers.DeclarativeContainer):
    repositories = providers.DependenciesContainer()

    domain_events = providers.Dict({GymAddedEvent: providers.Factory(GymAddedEventHandler)})
