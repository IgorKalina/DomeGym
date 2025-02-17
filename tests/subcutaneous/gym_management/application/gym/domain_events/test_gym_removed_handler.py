import uuid
from typing import TYPE_CHECKING

import pytest

from src.gym_management.domain.gym.aggregate_root import Gym
from src.gym_management.domain.room.aggregate_root import Room
from src.gym_management.domain.subscription import SubscriptionType
from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.shared_kernel.infrastructure.eventbus.eventbus_memory import DomainEventBusMemory
from tests.common.gym_management.common import constants
from tests.common.gym_management.gym.factory.gym_domain_event_factory import GymDomainEventFactory
from tests.common.gym_management.gym.factory.gym_factory import GymFactory
from tests.common.gym_management.gym.repository.memory import GymMemoryRepository
from tests.common.gym_management.room.factory.room_factory import RoomFactory
from tests.common.gym_management.room.repository.memory import RoomMemoryRepository
from tests.common.gym_management.subscription.factory.subscription_factory import SubscriptionFactory

if TYPE_CHECKING:
    from src.gym_management.domain.subscription.events.gym_removed_event import GymRemovedEvent


@pytest.mark.asyncio
class TestGymRemovedHandler:
    @pytest.fixture(autouse=True)
    def setup_method(
        self,
        domain_event_bus: DomainEventBusMemory,
        room_repository: RoomMemoryRepository,
        gym_repository: GymMemoryRepository,
    ) -> None:
        self._domain_eventbus = domain_event_bus
        self._room_repository = room_repository
        self._gym_repository = gym_repository
        self._rooms_count = 10

    async def test_when_removed_gym_has_rooms_should_remove_all(self, room: Room) -> None:
        # Arrange
        # room should stay untouched
        subscription: Subscription = SubscriptionFactory.create_subscription(type=SubscriptionType.PRO)
        gym: Gym = await self._create_gym(subscription)
        await self._add_rooms(gym)
        event: GymRemovedEvent = GymDomainEventFactory.create_gym_removed_event(subscription=subscription, gym=gym)

        # Act
        await self._domain_eventbus.publish([event])
        await self._domain_eventbus.process_events()

        # Assert
        actual_gym: Gym | None = await self._gym_repository.get_or_none(gym.id)
        assert actual_gym is None
        rooms_by_existing_gym = await self._room_repository.get_by_gym_id(room.gym_id)
        assert len(rooms_by_existing_gym) == 1
        existing_room = rooms_by_existing_gym[0]
        assert existing_room == room

    async def test_when_removed_gym_not_exists_should_do_nothing(self, room: Room) -> None:
        # Arrange
        # room_db should stay untouched
        subscription: Subscription = SubscriptionFactory.create_subscription()
        gym: Gym = GymFactory.create_gym(id=constants.common.NON_EXISTING_ID, subscription_id=subscription.id)
        event: GymRemovedEvent = GymDomainEventFactory.create_gym_removed_event(subscription=subscription, gym=gym)

        # Act
        await self._domain_eventbus.publish([event])
        await self._domain_eventbus.process_events()

        # Assert
        rooms_by_existing_gym = await self._room_repository.get_by_gym_id(room.gym_id)
        assert len(rooms_by_existing_gym) == 1
        existing_room = rooms_by_existing_gym[0]
        assert existing_room == room

    async def _create_gym(self, subscription: Subscription) -> Gym:
        gym: Gym = GymFactory.create_gym(
            id=uuid.uuid4(), subscription_id=subscription.id, max_rooms=subscription.max_rooms
        )
        await self._gym_repository.create(gym)
        return gym

    async def _add_rooms(self, gym: Gym) -> None:
        for _ in range(self._rooms_count):
            room = RoomFactory.create_room(id=uuid.uuid4(), gym_id=gym.id)
            await self._room_repository.create(room)
            gym.add_room(room)
            await self._gym_repository.update(gym)
