from src.gym_management.domain.gym.aggregate_root import Gym
from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.gym_management.domain.subscription.events.gym_added_event import GymAddedEvent
from src.gym_management.domain.subscription.events.gym_removed_event import GymRemovedEvent
from tests.common.gym_management.gym.factory.gym_factory import GymFactory
from tests.common.gym_management.subscription.factory.subscription_factory import SubscriptionFactory


class GymDomainEventFactory:
    @staticmethod
    def create_gym_added_event(
        subscription: Subscription | None = None,
        gym: Gym | None = None,
    ) -> GymAddedEvent:
        if subscription is None:
            subscription = SubscriptionFactory.create_subscription()
        if gym is None:
            gym = GymFactory.create_gym()
        return GymAddedEvent(subscription=subscription, gym=gym)

    @staticmethod
    def create_gym_removed_event(
        subscription: Subscription | None = None,
        gym: Gym | None = None,
    ) -> GymRemovedEvent:
        if subscription is None:
            subscription = SubscriptionFactory.create_subscription()
        if gym is None:
            gym = GymFactory.create_gym()
        return GymRemovedEvent(subscription=subscription, gym=gym)
