from src.shared_kernel.infrastructure.eventbus.interfaces.broker import EventHandler
from src.shared_kernel.infrastructure.eventbus.interfaces.subscriber import EventSubscriber


class DomainEventSubscriber(EventSubscriber):
    async def subscribe(self, handler: EventHandler) -> None:
        pass
