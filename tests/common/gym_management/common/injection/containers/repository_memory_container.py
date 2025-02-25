from dependency_injector import providers

from src.gym_management.infrastructure.common.injection.containers.repository.base import RepositoryContainer
from tests.common.gym_management.admin.repository.memory import AdminMemoryRepository
from tests.common.gym_management.common.repository_state_memory import RepositorySharedState
from tests.common.gym_management.common.unit_of_work_memory import UnitOfWorkMemory
from tests.common.gym_management.domain_event.repository.memory import DomainEventMemoryRepository
from tests.common.gym_management.gym.repository.memory import GymMemoryRepository
from tests.common.gym_management.room.repository.memory import RoomMemoryRepository
from tests.common.gym_management.subscription.repository.memory import (
    SubscriptionMemoryRepository,
)


class RepositoryMemoryContainer(RepositoryContainer):
    repository_shared_state = providers.Singleton(RepositorySharedState)

    unit_of_work = providers.Singleton(UnitOfWorkMemory)
    admin_repository = providers.Singleton(
        AdminMemoryRepository,
        shared_state=repository_shared_state,
    )
    subscription_repository = providers.Singleton(
        SubscriptionMemoryRepository,
        shared_state=repository_shared_state,
    )
    gym_repository = providers.Singleton(
        GymMemoryRepository,
        shared_state=repository_shared_state,
    )
    room_repository = providers.Singleton(
        RoomMemoryRepository,
        shared_state=repository_shared_state,
    )
    domain_event_repository = providers.Singleton(DomainEventMemoryRepository)
