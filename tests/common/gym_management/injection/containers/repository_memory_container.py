from dependency_injector import providers

from src.gym_management.infrastructure.common.injection.containers.repository_base import RepositoryContainer
from src.gym_management.infrastructure.common.postgres.repository.admin.repository_memory import AdminMemoryRepository
from src.gym_management.infrastructure.common.postgres.repository.gym.repository_memory import GymMemoryRepository
from src.gym_management.infrastructure.common.postgres.repository.room.repository_memory import RoomMemoryRepository
from src.gym_management.infrastructure.common.postgres.repository.subscription.repository_memory import (
    SubscriptionMemoryRepository,
)
from src.shared_kernel.infrastructure.event.domain.failed_events_tinydb_repository import (
    FailedDomainEventTinyDBRepository,
)


class RepositoryMemoryContainer(RepositoryContainer):
    admin_repository = providers.Singleton(AdminMemoryRepository)
    subscription_repository = providers.Singleton(SubscriptionMemoryRepository)
    gym_repository = providers.Singleton(GymMemoryRepository)
    room_repository = providers.Singleton(RoomMemoryRepository)
    failed_domain_event_repository = providers.Singleton(FailedDomainEventTinyDBRepository)
