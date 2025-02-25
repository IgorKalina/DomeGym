from dependency_injector import containers, providers

from src.gym_management.application.common.interfaces.repository.admin_repository import AdminRepository
from src.gym_management.application.common.interfaces.repository.domain_event_outbox_repository import (
    DomainEventRepository,
)
from src.gym_management.application.common.interfaces.repository.gym_repository import GymRepository
from src.gym_management.application.common.interfaces.repository.room_repository import RoomRepository
from src.gym_management.application.common.interfaces.repository.subscription_repository import SubscriptionRepository
from src.shared_kernel.infrastructure.interfaces.unit_of_work import UnitOfWork


class RepositoryContainer(containers.DeclarativeContainer):
    unit_of_work: providers.AbstractSingleton[UnitOfWork] = providers.AbstractSingleton()
    admin_repository: providers.AbstractSingleton[AdminRepository] = providers.AbstractSingleton()
    subscription_repository: providers.AbstractSingleton[SubscriptionRepository] = providers.AbstractSingleton()
    gym_repository: providers.AbstractSingleton[GymRepository] = providers.AbstractSingleton()
    room_repository: providers.AbstractSingleton[RoomRepository] = providers.AbstractSingleton()
    domain_event_repository: providers.AbstractSingleton[DomainEventRepository] = providers.AbstractSingleton()
