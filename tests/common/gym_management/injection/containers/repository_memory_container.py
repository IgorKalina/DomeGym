from dependency_injector import providers

from src.gym_management.infrastructure.admin.repository.repository_memory import AdminMemoryRepository
from src.gym_management.infrastructure.common.injection.containers.repository_base import RepositoryContainer
from src.gym_management.infrastructure.gym.repository.repository_memory import GymMemoryRepository
from src.gym_management.infrastructure.subscription.repository.repository_memory import SubscriptionMemoryRepository
from src.shared_kernel.infrastructure.event.domain.failed_events_tinydb_repository import (
    FailedDomainEventTinyDBRepository,
)


class RepositoryMemoryContainer(RepositoryContainer):
    admin_repository = providers.Singleton(AdminMemoryRepository)
    subscription_repository = providers.Singleton(SubscriptionMemoryRepository)
    gym_repository = providers.Singleton(GymMemoryRepository)
    failed_domain_event_repository = providers.Singleton(FailedDomainEventTinyDBRepository)
