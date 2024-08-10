from src.gym_management.application.dependency_injection.containers import CommandsContainer
from src.gym_management.application.gyms.commands.create_gym import CreateGym
from src.gym_management.application.subscriptions.commands.create_subscription import CreateSubscription
from src.shared_kernel.mediator.mediator import Mediator


async def setup_commands(
    mediator,
    commands: CommandsContainer,
) -> Mediator:
    mediator.register_command_handler(CreateSubscription, handler=await commands.create_subscription_handler())
    mediator.register_command_handler(CreateGym, handler=await commands.create_gym_handler())
    return mediator
