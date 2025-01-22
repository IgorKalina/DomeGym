from dependency_injector import providers

from src.gym_management.infrastructure.common.injection.containers.repository_base import RepositoryContainer
from src.shared_kernel.infrastructure.event.failed_events_tinydb_repository import (
    FailedDomainEventTinyDBRepository,
)
from tests.common.gym_management.admin.repository.memory import AdminMemoryRepository
from tests.common.gym_management.gym.repository.memory import GymMemoryRepository
from tests.common.gym_management.room.repository.memory import RoomMemoryRepository
from tests.common.gym_management.subscription.repository.memory import (
    SubscriptionMemoryRepository,
)


class RepositoryMemoryContainer(RepositoryContainer):
    admin_repository = providers.Singleton(AdminMemoryRepository)
    subscription_repository = providers.Singleton(SubscriptionMemoryRepository)
    gym_repository = providers.Singleton(GymMemoryRepository)
    room_repository = providers.Singleton(RoomMemoryRepository)
    failed_domain_event_repository = providers.Singleton(FailedDomainEventTinyDBRepository)
