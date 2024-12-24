from src.gym_management.domain.subscription.errors import SubscriptionCannotHaveMoreGymsThanSubscriptionAllows
from src.gym_management.domain.subscription.subscription_type import SubscriptionType
from tests.common.gym_management.gym.gym_factory import GymFactory
from tests.common.gym_management.subscription.factory.subscription_factory import SubscriptionFactory


class TestSubscriptionAggregate:
    def test_add_room_when_less_or_equal_than_subscription_allows_should_succeed(self) -> None:
        # Arrange
        subscription = SubscriptionFactory.create_subscription(subscription_type=SubscriptionType.PRO)
        gyms = [GymFactory.create_gym() for _ in range(subscription.max_gyms)]

        # Act
        add_gym_results = [subscription.add_gym(gym) for gym in gyms]

        # Assert
        assert all(r.is_ok() for r in add_gym_results)
        assert all(subscription.has_gym(gym.id) for gym in gyms)

    def test_add_room_when_more_than_subscription_allows_should_fail(self) -> None:
        # Arrange
        subscription = SubscriptionFactory.create_subscription(subscription_type=SubscriptionType.PRO)
        gyms = [GymFactory.create_gym() for _ in range(subscription.max_gyms + 1)]

        # Act
        add_gym_results = [subscription.add_gym(gym) for gym in gyms]

        # Assert
        add_gym_last_result = add_gym_results[-1]
        add_gym_results_before_last = add_gym_results[:-1]
        assert all(r.is_ok() for r in add_gym_results_before_last)
        assert add_gym_last_result.is_error()
        assert add_gym_last_result.first_error == SubscriptionCannotHaveMoreGymsThanSubscriptionAllows()
