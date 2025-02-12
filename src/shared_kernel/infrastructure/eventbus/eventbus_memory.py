import logging
import queue
from collections import defaultdict
from typing import Dict, List, Type

from src.shared_kernel.application.event.domain.event_bus import DomainEventBus
from src.shared_kernel.application.event.domain.repository import FailedDomainEventRepository
from src.shared_kernel.application.exceptions import EventHandlerAlreadyExistsError, EventualConsistencyError
from src.shared_kernel.domain.common.event import DomainEvent, DomainEventHandler

logger = logging.getLogger(__name__)


class DomainEventBusMemory(DomainEventBus):
    def __init__(self, event_repository: FailedDomainEventRepository) -> None:
        self.__domain_event_repository: FailedDomainEventRepository = event_repository

        self.__events_queue: queue.Queue[DomainEvent] = queue.Queue()
        self.__subscribers: Dict[Type[DomainEvent], List[DomainEventHandler]] = defaultdict(list)

    async def subscribe(self, event: Type[DomainEvent], handler: DomainEventHandler) -> None:
        if handler in self.__subscribers[event]:
            raise EventHandlerAlreadyExistsError(event=event, handler=handler)

        self.__subscribers[event].append(handler)
        logger.debug(f"Domain Event Handler '{handler.__class__.__name__}' is subscribed to '{event.__name__}' event")

    async def publish(self, events: List[DomainEvent]) -> None:
        for event in events:
            self.__events_queue.put(event)

    async def process_events(self) -> None:
        while not self.__events_queue.empty():
            await self.__process_next_event_from_queue()

    async def __process_next_event_from_queue(self) -> None:
        event: DomainEvent = self.__events_queue.get()
        subscribers: List[DomainEventHandler] = self.__subscribers[type(event)]
        for subscriber in subscribers:
            logger.info(
                f"Event '{event.__class__.__name__} is being handled by '{subscriber.__class__.__name__}' handler"
            )
            try:
                await subscriber.handle(event.model_copy(deep=True))
            except Exception as e:
                logger.exception(f"An error occurred while processing '{event}' domain event: {str(e)}")
                await self.__domain_event_repository.create(event)
                raise EventualConsistencyError() from e
