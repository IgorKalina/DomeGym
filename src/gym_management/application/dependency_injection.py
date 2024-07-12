from dependency_injector import containers, providers

from src.common.mediator.mediator import Mediator
from src.gym_management.application.gyms.commands.create_gym import CreateGym, CreateGymHandler
from src.gym_management.application.subscriptions.commands.create_subscription import (
    CreateSubscription,
    CreateSubscriptionHandler,
)
from src.gym_management.application.subscriptions.queries.list_subscriptions import (
    ListSubscriptions,
    ListSubscriptionsHandler,
)
from src.gym_management.infrastructure.dependency_injection import InfrastructureContainer


class CommandsContainer(containers.DeclarativeContainer):
    infrastructure = providers.DependenciesContainer()

    create_subscription_handler = providers.Factory(
        CreateSubscriptionHandler,
        admins_repository=infrastructure.admins_repository,
        subscriptions_repository=infrastructure.subscriptions_repository,
    )

    create_gym_handler = providers.Factory(
        CreateGymHandler,
        subscriptions_repository=infrastructure.subscriptions_repository,
    )


class QueriesContainer(containers.DeclarativeContainer):
    infrastructure = providers.DependenciesContainer()

    create_subscription_handler = providers.Factory(
        CreateSubscriptionHandler,
        admins_repository=infrastructure.admins_repository,
        subscriptions_repository=infrastructure.subscriptions_repository,
    )

    list_subscriptions_handler = providers.Factory(
        ListSubscriptionsHandler,
        subscriptions_repository=infrastructure.subscriptions_repository,
    )


class EventsContainer(containers.DeclarativeContainer):
    infrastructure = providers.DependenciesContainer()


def init_mediator(commands: CommandsContainer, queries: QueriesContainer, events: EventsContainer) -> Mediator:
    mediator = Mediator()
    setup_commands(mediator, commands)
    setup_queries(mediator, queries)
    setup_events(mediator, events)
    return mediator


def setup_commands(mediator, commands: CommandsContainer) -> Mediator:
    mediator.register_command_handler(CreateSubscription, commands.create_subscription_handler())
    mediator.register_command_handler(CreateGym, commands.create_gym_handler())
    return mediator


def setup_queries(mediator, queries: QueriesContainer) -> Mediator:
    mediator.register_query_handler(ListSubscriptions, queries.list_subscriptions_handler())
    return mediator


def setup_events(mediator, events: EventsContainer) -> Mediator:
    return mediator


class MediatorContainer(containers.DeclarativeContainer):
    commands = providers.DependenciesContainer()
    queries = providers.DependenciesContainer()
    events = providers.DependenciesContainer()

    mediator = providers.Resource(init_mediator, commands=commands, queries=queries, events=events)


class ApplicationContainer(containers.DeclarativeContainer):
    _infrastructure_container = providers.Container(InfrastructureContainer)

    _commands_container = providers.Container(CommandsContainer, infrastructure=_infrastructure_container)
    _queries_container = providers.Container(QueriesContainer, infrastructure=_infrastructure_container)
    _events_container = providers.Container(EventsContainer, infrastructure=_infrastructure_container)

    mediator = providers.Container(
        MediatorContainer,
        commands=_commands_container,
        queries=_queries_container,
        events=_events_container,
    )
