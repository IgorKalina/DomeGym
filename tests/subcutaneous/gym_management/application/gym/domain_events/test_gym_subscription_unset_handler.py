import uuid
from typing import TYPE_CHECKING, List

import pytest

from src.gym_management.domain.gym.aggregate_root import Gym
from src.shared_kernel.infrastructure.eventbus.eventbus_memory import DomainEventBusMemory
from tests.common.gym_management.common import constants
from tests.common.gym_management.gym.factory.gym_factory import GymFactory
from tests.common.gym_management.gym.repository.memory import GymMemoryRepository
from tests.common.gym_management.subscription.factory.subscription_domain_event_factory import (
    SubscriptionDomainEventFactory,
)
from tests.common.gym_management.subscription.factory.subscription_factory import SubscriptionFactory
from tests.common.gym_management.subscription.repository.memory import SubscriptionMemoryRepository

if TYPE_CHECKING:
    from src.gym_management.domain.admin.events.subscription_unset_event import SubscriptionUnsetEvent
    from src.gym_management.domain.subscription.aggregate_root import Subscription


@pytest.mark.asyncio
class TestGymSubscriptionUnsetHandler:
    @pytest.fixture(autouse=True)
    def setup_method(
        self,
        domain_event_bus: DomainEventBusMemory,
        gym_repository: GymMemoryRepository,
        subscription_repository: SubscriptionMemoryRepository,
    ) -> None:
        self._domain_eventbus = domain_event_bus
        self._gym_repository = gym_repository
        self._subscription_repository = subscription_repository

        self._gyms_count = 10

    async def test_when_unset_subscription_has_gyms_should_remove_all(self, gym: Gym) -> None:
        # Arrange
        # gym_db should stay untouched
        subscription_id = uuid.uuid4()
        gyms: List[Gym] = await self._create_gyms(subscription_id)
        subscription: Subscription = SubscriptionFactory.create_subscription(
            id=subscription_id, gym_ids=[gym.id for gym in gyms]
        )
        await self._subscription_repository.create(subscription)
        event: SubscriptionUnsetEvent = SubscriptionDomainEventFactory.create_subscription_unset_event(
            subscription=subscription
        )

        # Act
        await self._domain_eventbus.publish([event])
        await self._domain_eventbus.process_events()

        # Assert

        gyms_by_unset_subscription = await self._gym_repository.get_by_subscription_id(event.subscription.id)
        assert len(gyms_by_unset_subscription) == 0
        gyms_by_existing_subscription = await self._gym_repository.get_by_subscription_id(gym.subscription_id)
        assert len(gyms_by_existing_subscription) == 1
        existing_gym = gyms_by_existing_subscription[0]
        assert existing_gym == gym

        assert len(await self._gym_repository.get_by_subscription_id(event.subscription.id)) == 0

    async def test_when_unset_subscription_not_exists_should_do_nothing(self, gym: Gym) -> None:
        # Arrange
        # gym_db should stay untouched
        subscription: Subscription = SubscriptionFactory.create_subscription(id=constants.common.NON_EXISTING_ID)
        event: SubscriptionUnsetEvent = SubscriptionDomainEventFactory.create_subscription_unset_event(
            subscription=subscription
        )

        # Act
        await self._domain_eventbus.publish([event])
        await self._domain_eventbus.process_events()

        # Assert
        gyms_by_existing_subscription = await self._gym_repository.get_by_subscription_id(gym.subscription_id)
        assert len(gyms_by_existing_subscription) == 1
        existing_gym = gyms_by_existing_subscription[0]
        assert existing_gym == gym

        assert len(await self._gym_repository.get_by_subscription_id(event.subscription.id)) == 0

    async def _create_gyms(self, subscription_id: uuid.UUID) -> List[Gym]:
        gyms: List[Gym] = []
        for _ in range(self._gyms_count):
            gym = GymFactory.create_gym(id=uuid.uuid4(), subscription_id=subscription_id)
            await self._gym_repository.create(gym)
            gyms.append(gym)
        return gyms
