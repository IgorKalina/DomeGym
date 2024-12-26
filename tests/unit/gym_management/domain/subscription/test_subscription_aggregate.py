import pytest

from src.gym_management.domain.subscription.exceptions import SubscriptionCannotHaveMoreGymsThanSubscriptionAllowsError
from src.gym_management.domain.subscription.subscription_type import SubscriptionType
from src.shared_kernel.application.error_or import ErrorType
from tests.common.gym_management.gym.factory.gym_factory import GymFactory
from tests.common.gym_management.subscription.factory.subscription_factory import SubscriptionFactory


class TestSubscriptionAggregate:
    def test_add_gym_when_less_or_equal_than_subscription_allows_should_succeed(self) -> None:
        # Arrange
        subscription = SubscriptionFactory.create_subscription(subscription_type=SubscriptionType.PRO)
        gyms_allowed = [GymFactory.create_gym() for _ in range(subscription.max_gyms)]

        # Act
        for gym in gyms_allowed:
            subscription.add_gym(gym)

        # Assert
        assert all(subscription.has_gym(gym.id) for gym in gyms_allowed)

    def test_add_gym_when_more_than_subscription_allows_should_fail(self) -> None:
        # Arrange
        subscription = SubscriptionFactory.create_subscription(subscription_type=SubscriptionType.PRO)
        gyms_allowed = [GymFactory.create_gym() for _ in range(subscription.max_gyms)]
        for gym in gyms_allowed:
            subscription.add_gym(gym=gym)

        # Act
        with pytest.raises(SubscriptionCannotHaveMoreGymsThanSubscriptionAllowsError) as err:
            subscription.add_gym(GymFactory.create_gym())

        # Assert
        assert err.value.max_gyms == subscription.max_gyms
        assert err.value.title == "Subscription.Validation"
        assert (
            err.value.detail
            == f"A subscription cannot have more gyms than the subscription allows ({subscription.max_gyms})"
        )
        assert err.value.error_type == ErrorType.VALIDATION
        assert all(subscription.has_gym(gym.id) for gym in gyms_allowed)
