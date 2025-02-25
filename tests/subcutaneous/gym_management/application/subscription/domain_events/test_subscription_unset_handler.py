import uuid
from typing import TYPE_CHECKING, List

import pytest

from src.gym_management.application.common.dto.repository.domain_event_outbox.domain_event_processing_status import (
    DomainEventProcessingStatus,
)
from src.gym_management.domain.gym.aggregate_root import Gym
from src.gym_management.domain.subscription.events.gym_removed_event import GymRemovedEvent
from src.shared_kernel.infrastructure.domain_event.domain_event_bus_memory import DomainEventBusMemory
from tests.common.gym_management.common import constants
from tests.common.gym_management.domain_event.repository.memory import DomainEventMemoryRepository
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
class TestSubscriptionUnsetHandler:
    @pytest.fixture(autouse=True)
    def setup_method(
        self,
        domain_event_bus: DomainEventBusMemory,
        gym_repository: GymMemoryRepository,
        subscription_repository: SubscriptionMemoryRepository,
        domain_event_repository: DomainEventMemoryRepository,
    ) -> None:
        self._domain_eventbus = domain_event_bus
        self._gym_repository = gym_repository
        self._subscription_repository = subscription_repository
        self._domain_event_repository = domain_event_repository

        self._gyms_count = 10

    async def test_when_unset_subscription_has_gyms_should_create_gym_removed_domain_events_for_all(
        self,
        gym: Gym,  # noqa: ARG002
    ) -> None:
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
        await self._domain_eventbus.publish(event)

        # Assert
        actual_subscription = await self._subscription_repository.get_or_none(event.subscription.id)
        assert actual_subscription is None
        domain_events = await self._domain_event_repository.list(status=DomainEventProcessingStatus.PENDING)
        assert len(domain_events) == self._gyms_count
        assert all(isinstance(dto.event, GymRemovedEvent) for dto in domain_events)
        assert [dto.event.gym for dto in domain_events] == gyms
        assert all(dto.event.subscription == subscription for dto in domain_events)

    async def test_when_unset_subscription_not_exists_should_do_nothing(self, gym: Gym) -> None:
        # Arrange
        # gym_db should stay untouched
        subscription: Subscription = SubscriptionFactory.create_subscription(id=constants.common.NON_EXISTING_ID)
        event: SubscriptionUnsetEvent = SubscriptionDomainEventFactory.create_subscription_unset_event(
            subscription=subscription
        )

        # Act
        await self._domain_eventbus.publish(event)

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
