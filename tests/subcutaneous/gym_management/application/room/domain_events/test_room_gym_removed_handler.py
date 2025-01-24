import uuid
from typing import TYPE_CHECKING, List

import pytest

from src.gym_management.application.common.dto.repository import RoomDB
from src.shared_kernel.infrastructure.event.eventbus_memory import DomainEventBusMemory
from tests.common.gym_management.common import constants
from tests.common.gym_management.gym.factory.gym_domain_event_factory import GymDomainEventFactory
from tests.common.gym_management.gym.factory.gym_factory import GymFactory
from tests.common.gym_management.room.factory.room_db_factory import RoomDBFactory
from tests.common.gym_management.room.repository.memory import RoomMemoryRepository
from tests.common.gym_management.subscription.factory.subscription_factory import SubscriptionFactory

if TYPE_CHECKING:
    from src.gym_management.domain.gym.aggregate_root import Gym
    from src.gym_management.domain.subscription.aggregate_root import Subscription
    from src.gym_management.domain.subscription.events.gym_removed_event import GymRemovedEvent


@pytest.mark.asyncio
class TestRoomGymRemovedHandler:
    @pytest.fixture(autouse=True)
    def setup_method(
        self,
        domain_eventbus: DomainEventBusMemory,
        room_repository: RoomMemoryRepository,
    ) -> None:
        self._domain_eventbus = domain_eventbus
        self._room_repository = room_repository
        self._rooms_count = 10

    async def test_when_removed_gym_has_rooms_should_remove_all(self, room_db: RoomDB) -> None:
        # Arrange
        # room_db should stay untouched
        gym_id = uuid.uuid4()
        subscription: Subscription = SubscriptionFactory.create_subscription(gym_ids=[gym_id])
        rooms: List[RoomDB] = await self._create_rooms(gym_id=gym_id)
        gym: Gym = GymFactory.create_gym(
            id=gym_id, room_ids=[room.id for room in rooms], subscription_id=subscription.id
        )
        event: GymRemovedEvent = GymDomainEventFactory.create_gym_removed_event(subscription=subscription, gym=gym)

        # Act
        await self._domain_eventbus.publish([event])
        await self._domain_eventbus.process_events()

        # Assert
        rooms_by_removed_gym = await self._room_repository.get_by_gym_id(gym_id)
        assert len(rooms_by_removed_gym) == 0
        rooms_by_existing_gym = await self._room_repository.get_by_gym_id(room_db.gym_id)
        assert len(rooms_by_existing_gym) == 1
        existing_room = rooms_by_existing_gym[0]
        assert existing_room == room_db

    async def test_when_removed_gym_not_exists_should_do_nothing(self, room_db: RoomDB) -> None:
        # Arrange
        # room_db should stay untouched
        subscription: Subscription = SubscriptionFactory.create_subscription()
        gym: Gym = GymFactory.create_gym(id=constants.common.NON_EXISTING_ID, subscription_id=subscription.id)
        event: GymRemovedEvent = GymDomainEventFactory.create_gym_removed_event(subscription=subscription, gym=gym)

        # Act
        await self._domain_eventbus.publish([event])
        await self._domain_eventbus.process_events()

        # Assert
        rooms_by_existing_gym = await self._room_repository.get_by_gym_id(room_db.gym_id)
        assert len(rooms_by_existing_gym) == 1
        existing_room = rooms_by_existing_gym[0]
        assert existing_room == room_db

    async def _create_rooms(self, gym_id: uuid.UUID) -> List[RoomDB]:
        rooms: List[RoomDB] = []
        for _ in range(self._rooms_count):
            room = RoomDBFactory.create_room(id=uuid.uuid4(), gym_id=gym_id)
            await self._room_repository.create(room)
            rooms.append(room)
        return rooms
