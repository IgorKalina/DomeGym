import pytest

from src.gym_management.domain.subscription.events.gym_added_event import GymAddedEvent
from src.gym_management.domain.subscription.exceptions import SubscriptionCannotHaveMoreGymsThanSubscriptionAllowsError
from src.gym_management.domain.subscription.subscription_type import SubscriptionType
from tests.common.gym_management.gym.factory.gym_factory import GymFactory
from tests.common.gym_management.subscription.factory.subscription_factory import SubscriptionFactory


class TestSubscriptionDomainEvents:
    def test_subscription_add_gym_when_added_should_create_domain_event(self) -> None:
        # Arrange
        subscription = SubscriptionFactory.create_subscription(type=SubscriptionType.PRO)
        gyms = [GymFactory.create_gym() for _ in range(subscription.max_gyms)]
        expected_domain_events = [
            GymAddedEvent(
                subscription=subscription,
                gym=gym,
            )
            for gym in gyms
        ]

        # Act
        for gym in gyms:
            subscription.add_gym(gym)

        # Assert
        assert subscription.pop_domain_events() == expected_domain_events

    def test_subscription_add_gym_when_error_should_not_create_domain_event(self) -> None:
        # Arrange
        subscription = SubscriptionFactory.create_subscription(type=SubscriptionType.PRO)
        gyms = [GymFactory.create_gym() for _ in range(subscription.max_gyms)]
        for gym in gyms:
            subscription.add_gym(gym)
        # flush domain events created for valid number of gyms
        subscription.pop_domain_events()

        # Act
        with pytest.raises(SubscriptionCannotHaveMoreGymsThanSubscriptionAllowsError):
            subscription.add_gym(GymFactory.create_gym())

        # Assert
        assert subscription.pop_domain_events() == []
