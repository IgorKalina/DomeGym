from src.gym_management.domain.subscription.events.gym_added_event import GymAddedEvent
from src.gym_management.domain.subscription.subscription_type import SubscriptionType
from tests.common.gym_management.gym.gym_factory import GymFactory
from tests.common.gym_management.subscription.subscription_factory import SubscriptionFactory


class TestSubscriptionDomainEvents:
    def test_subscription_add_gym_when_added_should_create_domain_event(self) -> None:
        subscription = SubscriptionFactory.create_subscription(subscription_type=SubscriptionType.PRO)
        gyms = [GymFactory.create_gym() for _ in range(subscription.max_gyms)]

        for gym in gyms:
            subscription.add_gym(gym)

        expected_domain_events = [
            GymAddedEvent(
                subscription=subscription,
                gym=gym,
            )
            for gym in gyms
        ]

        assert subscription.pop_domain_events() == expected_domain_events

    def test_subscription_add_gym_when_error_should_not_create_domain_event(self) -> None:
        subscription = SubscriptionFactory.create_subscription(subscription_type=SubscriptionType.PRO)
        gyms = [GymFactory.create_gym() for _ in range(subscription.max_gyms)]
        for gym in gyms:
            subscription.add_gym(gym)
        # flush domain events created for valid number of gyms
        subscription.pop_domain_events()

        subscription.add_gym(GymFactory.create_gym())

        assert subscription.pop_domain_events() == []
