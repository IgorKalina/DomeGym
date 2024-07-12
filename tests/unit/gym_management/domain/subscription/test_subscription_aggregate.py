from src.gym_management.domain.subscription.errors import SubscriptionCannotHaveMoreGymsThanSubscriptionAllows
from src.gym_management.domain.subscription.events.gym_added_event import GymAddedEvent
from src.gym_management.domain.subscription.subscription_type import SubscriptionType
from tests.unit.utils.gym.gym_factory import GymFactory
from tests.unit.utils.subscription.subscription_factory import SubscriptionFactory


class TestSubscriptionAggregate:
    def test_add_room_when_less_or_equal_than_subscription_allows_should_succeed(self) -> None:
        subscription = SubscriptionFactory.create_subscription(subscription_type=SubscriptionType.PRO)
        gyms = [GymFactory.create_gym() for _ in range(subscription.max_gyms)]

        add_gym_results = [subscription.add_gym(gym) for gym in gyms]
        assert all([r.is_ok() for r in add_gym_results])
        assert all([subscription.has_gym(gym.id) for gym in gyms])
        expected_domain_events = [
            GymAddedEvent(
                subscription=subscription,
                gym=gym,
            )
            for gym in gyms
        ]

        actual_domain_events = subscription.pop_domain_events()
        assert actual_domain_events == expected_domain_events

    def test_add_room_when_more_than_subscription_allows_should_fail(self) -> None:
        subscription = SubscriptionFactory.create_subscription(subscription_type=SubscriptionType.PRO)
        gyms = [GymFactory.create_gym() for _ in range(subscription.max_gyms + 1)]

        add_gym_results = [subscription.add_gym(gym) for gym in gyms]

        add_gym_last_result = add_gym_results[-1]
        add_gym_results_before_last = add_gym_results[:-1]
        assert all([r.is_ok() for r in add_gym_results_before_last])
        assert add_gym_last_result.is_error()
        assert add_gym_last_result.first_error == SubscriptionCannotHaveMoreGymsThanSubscriptionAllows()
        expected_domain_events = [
            GymAddedEvent(
                subscription=subscription,
                gym=gym,
            )
            for gym in gyms[:-1]
        ]

        actual_domain_events = subscription.pop_domain_events()
        assert actual_domain_events == expected_domain_events
