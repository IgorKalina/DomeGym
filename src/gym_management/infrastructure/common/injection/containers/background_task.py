from dependency_injector import containers, providers

from src.gym_management.infrastructure.common.background_services.domain_events.cronjob.publish_domain_events import (
    publish_domain_events,
)
from src.gym_management.infrastructure.common.injection.containers.eventbus.base import EventbusContainer
from src.gym_management.infrastructure.common.injection.containers.repository.base import RepositoryContainer


class BackgroundTaskContainer(containers.DeclarativeContainer):
    repository_container: RepositoryContainer = providers.DependenciesContainer()
    eventbus_container: EventbusContainer = providers.DependenciesContainer()

    publish_domain_events = providers.Factory(
        publish_domain_events,
        domain_event_outbox_repository=repository_container.domain_event_outbox_repository,
        event_publisher=eventbus_container.domain_event_publisher,
    )
