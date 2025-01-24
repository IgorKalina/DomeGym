import pytest

from src.gym_management.application.common.dto.repository import RoomDB
from src.gym_management.application.common.dto.repository.gym import GymDB
from src.gym_management.application.common.dto.repository.subscription import SubscriptionDB
from src.gym_management.infrastructure.common.injection.main import DiContainer
from src.shared_kernel.infrastructure.command.command_invoker_memory import CommandInvokerMemory
from src.shared_kernel.infrastructure.query.query_invoker_memory import QueryInvokerMemory
from tests.common.gym_management.admin.factory.admin_db_factory import AdminDBFactory
from tests.common.gym_management.admin.repository.memory import AdminMemoryRepository
from tests.common.gym_management.common.injection.containers.repository_memory_container import (
    RepositoryMemoryContainer,
)
from tests.common.gym_management.gym.factory.gym_db_factory import GymDBFactory
from tests.common.gym_management.gym.repository.memory import GymMemoryRepository
from tests.common.gym_management.room.factory.room_db_factory import RoomDBFactory
from tests.common.gym_management.room.repository.memory import RoomMemoryRepository
from tests.common.gym_management.subscription.factory.subscription_db_factory import SubscriptionDBFactory
from tests.common.gym_management.subscription.repository.memory import (
    SubscriptionMemoryRepository,
)


@pytest.fixture
async def di_container() -> DiContainer:
    return DiContainer(repository_container=RepositoryMemoryContainer())


@pytest.fixture
async def command_invoker(di_container: DiContainer) -> CommandInvokerMemory:
    return await di_container.command_invoker()


@pytest.fixture
async def query_invoker(di_container: DiContainer) -> QueryInvokerMemory:
    return await di_container.query_invoker()


@pytest.fixture
async def domain_eventbus(di_container: DiContainer) -> QueryInvokerMemory:
    return await di_container.domain_eventbus()


@pytest.fixture
def admin_repository(di_container: DiContainer) -> AdminMemoryRepository:
    return di_container.repository_container.admin_repository()


@pytest.fixture
def subscription_repository(di_container: DiContainer) -> SubscriptionMemoryRepository:
    return di_container.repository_container.subscription_repository()


@pytest.fixture
def gym_repository(di_container: DiContainer) -> GymMemoryRepository:
    return di_container.repository_container.gym_repository()


@pytest.fixture
def room_repository(di_container: DiContainer) -> RoomMemoryRepository:
    return di_container.repository_container.room_repository()


@pytest.fixture
async def subscription_db(
    subscription_repository: SubscriptionMemoryRepository,
) -> SubscriptionDB:
    subscription = SubscriptionDBFactory.create_subscription()
    await subscription_repository.create(subscription)
    return subscription


@pytest.fixture
async def admin_db_with_subscription(
    subscription_db: SubscriptionDB, admin_repository: AdminMemoryRepository
) -> SubscriptionDB:
    admin = AdminDBFactory.create_admin(subscription_id=subscription_db.id)
    await admin_repository.create(admin)
    return admin


@pytest.fixture
async def admin_db_no_subscription(admin_repository: AdminMemoryRepository) -> SubscriptionDB:
    admin = AdminDBFactory.create_admin(subscription_id=None)
    await admin_repository.create(admin)
    return admin


@pytest.fixture
async def gym_db(subscription_db: SubscriptionDB, gym_repository: GymMemoryRepository) -> GymDB:
    gym: GymDB = GymDBFactory.create_gym(subscription_id=subscription_db.id)
    await gym_repository.create(gym)
    return gym


@pytest.fixture
async def room_db(gym_db: GymDB, room_repository: RoomMemoryRepository) -> RoomDB:
    room: RoomDB = RoomDBFactory.create_room(gym_id=gym_db.id, subscription_id=gym_db.subscription_id)
    await room_repository.create(room)
    return room
