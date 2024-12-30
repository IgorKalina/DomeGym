from dependency_injector import containers, providers

from src.gym_management.application.room.domain_events.gym_added_handler import GymAddedEventHandler
from src.gym_management.application.subscription.commands.create_subscription import (
    CreateSubscription,
    CreateSubscriptionHandler,
)
from src.gym_management.application.subscription.queries.list_subscriptions import (
    ListSubscriptions,
    ListSubscriptionsHandler,
)
from src.gym_management.domain.admin.events.subscription_set_event import SubscriptionSetEvent
from src.shared_kernel.application.event.eventbus import EventBus


class SubscriptionsContainer(containers.DeclarativeContainer):
    repositories = providers.DependenciesContainer()
    domain_eventbus = providers.Dependency(instance_of=EventBus)

    commands = providers.Dict(
        {
            CreateSubscription: providers.Factory(
                CreateSubscriptionHandler,
                admin_repository=repositories.admin_repository,
                subscription_repository=repositories.subscription_repository,
                eventbus=domain_eventbus,
            )
        }
    )

    queries = providers.Dict(
        {
            ListSubscriptions: providers.Factory(
                ListSubscriptionsHandler, subscription_repository=repositories.subscription_repository
            )
        }
    )

    domain_events = providers.Dict({SubscriptionSetEvent: providers.Factory(GymAddedEventHandler)})
