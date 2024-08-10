from src.gym_management.application.dependency_injection.containers import EventsContainer
from src.shared_kernel.mediator.mediator import Mediator


async def setup_events(mediator, events: EventsContainer) -> Mediator:
    return mediator
