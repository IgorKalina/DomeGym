from dependency_injector import containers, providers

from src.gym_management.application.gyms.commands.create_gym import CreateGym
from src.gym_management.application.subscriptions.commands.create_subscription import (
    CreateSubscription,
)
from src.gym_management.infrastructure.subscriptions.injection.commands import SubscriptionCommandsContainer
from src.shared_kernel.application.command.command_invoker_memory import CommandInvokerMemory


def init_subscriptions_command_invoker(
    commands_invoker: CommandInvokerMemory, subscriptions_commands: SubscriptionCommandsContainer
) -> CommandInvokerMemory:
    commands_invoker.register_command_handler(CreateGym, subscriptions_commands.create_gym_handler())
    commands_invoker.register_command_handler(CreateSubscription, subscriptions_commands.create_subscription_handler())
    return commands_invoker


class SubscriptionsContainer(containers.DeclarativeContainer):
    commands_invoker = providers.Resource(
        init_subscriptions_command_invoker,
        commands_invoker=providers.Singleton(CommandInvokerMemory),
        subscriptions_commands=providers.Container(SubscriptionCommandsContainer),
    )
