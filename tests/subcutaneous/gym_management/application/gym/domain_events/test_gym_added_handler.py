from typing import TYPE_CHECKING

import pytest

from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.shared_kernel.infrastructure.eventbus.eventbus_memory import DomainEventBusMemory
from tests.common.gym_management.common import constants
from tests.common.gym_management.gym.factory.gym_domain_event_factory import GymDomainEventFactory
from tests.common.gym_management.gym.factory.gym_factory import GymFactory
from tests.common.gym_management.gym.repository.memory import GymMemoryRepository
from tests.common.gym_management.subscription.factory.subscription_factory import SubscriptionFactory
from tests.common.gym_management.subscription.repository.memory import SubscriptionMemoryRepository

if TYPE_CHECKING:
    from src.gym_management.domain.gym.aggregate_root import Gym
    from src.gym_management.domain.subscription.events.gym_added_event import GymAddedEvent


@pytest.mark.asyncio
class TestGymAddedHandler:
    @pytest.fixture(autouse=True)
    def setup_method(
        self,
        domain_event_bus: DomainEventBusMemory,
        subscription_repository: SubscriptionMemoryRepository,
        gym_repository: GymMemoryRepository,
    ) -> None:
        self._domain_eventbus = domain_event_bus
        self._subscription_repository = subscription_repository
        self._gym_repository = gym_repository
        self._rooms_count = 10

    async def test_when_gym_not_exists_should_create_gym(self, subscription: Subscription) -> None:
        # Arrange
        gym: Gym = GymFactory.create_gym(subscription_id=subscription.id, max_rooms=subscription.max_rooms)
        subscription.add_gym(gym)
        await self._subscription_repository.update(subscription)
        event: GymAddedEvent = GymDomainEventFactory.create_gym_added_event(subscription=subscription, gym=gym)

        # Act
        await self._domain_eventbus.publish([event])
        await self._domain_eventbus.process_events()

        # Assert
        actual_gym: Gym | None = await self._gym_repository.get_or_none(gym.id)
        assert actual_gym is not None
        assert actual_gym == gym

    async def test_when_event_sent_twice_should_do_nothing(self) -> None:
        # Arrange
        subscription: Subscription = SubscriptionFactory.create_subscription()
        gym: Gym = GymFactory.create_gym(id=constants.common.NON_EXISTING_ID, subscription_id=subscription.id)
        event: GymAddedEvent = GymDomainEventFactory.create_gym_added_event(subscription=subscription, gym=gym)

        # Act
        await self._domain_eventbus.publish([event, event])
        await self._domain_eventbus.process_events()

        # Assert
        actual_gym: Gym | None = await self._gym_repository.get_or_none(gym.id)
        assert actual_gym is not None
        assert actual_gym == gym
