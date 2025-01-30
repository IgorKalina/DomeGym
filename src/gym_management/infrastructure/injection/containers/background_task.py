from dependency_injector import containers, providers

from src.gym_management.infrastructure.background_services.cronjob.publish_domain_events import publish_domain_events
from src.gym_management.infrastructure.injection.containers.repository_base import RepositoryContainer


class BackgroundTaskContainer(containers.DeclarativeContainer):
    repository_container: RepositoryContainer = providers.DependenciesContainer()

    publish_domain_events = providers.Factory(
        publish_domain_events, domain_event_outbox_repository=repository_container.domain_event_outbox_repository
    )
