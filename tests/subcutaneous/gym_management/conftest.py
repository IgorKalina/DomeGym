from typing import TYPE_CHECKING, AsyncGenerator

import pytest

from src.gym_management.application.common.dto.repository import RoomDB
from src.gym_management.domain.admin.aggregate_root import Admin
from src.gym_management.domain.gym.aggregate_root import Gym
from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.shared_kernel.infrastructure.command.command_bus_memory import CommandBusMemory
from src.shared_kernel.infrastructure.query.query_bus_memory import QueryBusMemory
from tests.common.gym_management.admin.factory.admin_factory import AdminFactory
from tests.common.gym_management.admin.repository.memory import AdminMemoryRepository
from tests.common.gym_management.common.injection.main import DiMemoryContainer
from tests.common.gym_management.domain_event.repository.memory import DomainEventMemoryRepository
from tests.common.gym_management.gym.factory.gym_factory import GymFactory
from tests.common.gym_management.gym.repository.memory import GymMemoryRepository
from tests.common.gym_management.room.factory.room_factory import RoomFactory
from tests.common.gym_management.room.repository.memory import RoomMemoryRepository
from tests.common.gym_management.subscription.factory.subscription_factory import SubscriptionFactory
from tests.common.gym_management.subscription.repository.memory import (
    SubscriptionMemoryRepository,
)

if TYPE_CHECKING:
    from src.gym_management.domain.room.aggregate_root import Room


@pytest.fixture
async def di_memory() -> AsyncGenerator[DiMemoryContainer, None]:
    di_memory = DiMemoryContainer()
    di_memory.init_resources()

    yield di_memory

    di_memory.shutdown_resources()


@pytest.fixture
async def command_bus(di_memory: DiMemoryContainer) -> CommandBusMemory:
    return await di_memory.command_container.command_bus()


@pytest.fixture
async def query_bus(di_memory: DiMemoryContainer) -> QueryBusMemory:
    return await di_memory.query_container.query_bus()


@pytest.fixture
async def domain_event_bus(di_memory: DiMemoryContainer) -> QueryBusMemory:
    return await di_memory.domain_event_container.domain_event_bus()


@pytest.fixture
def admin_repository(di_memory: DiMemoryContainer) -> AdminMemoryRepository:
    return di_memory.repository_container.admin_repository()


@pytest.fixture
def subscription_repository(di_memory: DiMemoryContainer) -> SubscriptionMemoryRepository:
    return di_memory.repository_container.subscription_repository()


@pytest.fixture
def gym_repository(di_memory: DiMemoryContainer) -> GymMemoryRepository:
    return di_memory.repository_container.gym_repository()


@pytest.fixture
def domain_event_repository(di_memory: DiMemoryContainer) -> DomainEventMemoryRepository:
    return di_memory.repository_container.domain_event_repository()


@pytest.fixture
def room_repository(di_memory: DiMemoryContainer) -> RoomMemoryRepository:
    return di_memory.repository_container.room_repository()


@pytest.fixture
async def subscription(
    subscription_repository: SubscriptionMemoryRepository,
) -> Subscription:
    subscription = SubscriptionFactory.create_subscription()
    await subscription_repository.create(subscription)
    return subscription


@pytest.fixture
async def admin_with_subscription(subscription: Subscription, admin_repository: AdminMemoryRepository) -> Admin:
    admin = AdminFactory.create_admin(subscription_id=subscription.id)
    await admin_repository.create(admin)
    admin.set_subscription(subscription)
    return admin


@pytest.fixture
async def admin_without_subscription(admin_repository: AdminMemoryRepository) -> Admin:
    admin = AdminFactory.create_admin(subscription_id=None)
    await admin_repository.create(admin)
    return admin


@pytest.fixture
async def gym(subscription: Subscription, gym_repository: GymMemoryRepository) -> Gym:
    gym: Gym = GymFactory.create_gym(subscription_id=subscription.id)
    await gym_repository.create(gym)
    return gym


@pytest.fixture
async def room(gym: Gym, room_repository: RoomMemoryRepository) -> RoomDB:
    room: Room = RoomFactory.create_room(gym_id=gym.id)
    await room_repository.create(room)
    return room
