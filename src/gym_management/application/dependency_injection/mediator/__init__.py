from src.gym_management.application.dependency_injection.containers import (
    CommandsContainer,
    EventsContainer,
    QueriesContainer,
)
from src.shared_kernel.mediator.mediator import Mediator

from .setup_commands import setup_commands
from .setup_events import setup_events
from .setup_queries import setup_queries

__all__ = [
    "init_mediator",
]


async def init_mediator(commands: CommandsContainer, queries: QueriesContainer, events: EventsContainer) -> Mediator:
    mediator = Mediator()
    await setup_commands(mediator, commands)
    await setup_queries(mediator, queries)
    await setup_events(mediator, events)
    return mediator
