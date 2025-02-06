from src.shared_kernel.domain.common.event import DomainEvent
from src.shared_kernel.infrastructure.eventbus.interfaces.publisher import EventPublisher


class DomainEventPublisher(EventPublisher):
    async def publish(self, event: DomainEvent) -> None:
        pass
