import logging
import queue
from collections import defaultdict
from typing import Dict, List, Type

from src.shared_kernel.application.event.eventbus import EventBus
from src.shared_kernel.application.exceptions import EventHandlerAlreadyExistsError
from src.shared_kernel.domain.event import DomainEvent, DomainEventHandler

logger = logging.getLogger(__name__)


class DomainEventBusMemory(EventBus):
    def __init__(self) -> None:
        self.__events_queue: queue.Queue[DomainEvent] = queue.Queue()
        self.__subscribers: Dict[Type[DomainEvent], List[DomainEventHandler]] = defaultdict(list)

    async def subscribe(self, event: Type[DomainEvent], handler: DomainEventHandler) -> None:
        if handler in self.__subscribers[event]:
            raise EventHandlerAlreadyExistsError(event=event, handler=handler)

        self.__subscribers[event].append(handler)
        logger.debug(f"Domain Event Handler '{handler.__class__.__name__}' is subscribed to '{event.__name__}'")

    async def publish(self, events: List[DomainEvent]) -> None:
        for event in events:
            self.__events_queue.put(event)

    async def process_events(self) -> None:
        while not self.__events_queue.empty():
            event = self.__events_queue.get()
            subscribers = self.__subscribers[type(event)]
            for subscriber in subscribers:
                logger.info(f"Handler '{subscriber.__class__.__name__}' is handling event '{event.__class__.__name__}'")
                await subscriber.handle(event)
