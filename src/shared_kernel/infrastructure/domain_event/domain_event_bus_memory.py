import logging
from collections import defaultdict
from typing import Dict, List, Type

from src.shared_kernel.application.event.domain.event_bus import DomainEventBus
from src.shared_kernel.application.exceptions import EventHandlerAlreadyExistsError, EventualConsistencyError
from src.shared_kernel.domain.common.event import DomainEvent, DomainEventHandler
from src.shared_kernel.infrastructure.interfaces.unit_of_work import UnitOfWork

logger = logging.getLogger(__name__)


class DomainEventBusMemory(DomainEventBus):
    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self.__unit_of_work: UnitOfWork = unit_of_work
        self.__subscribers: Dict[Type[DomainEvent], List[DomainEventHandler]] = defaultdict(list)

    async def subscribe(self, event: Type[DomainEvent], handler: DomainEventHandler) -> None:
        if handler in self.__subscribers[event]:
            raise EventHandlerAlreadyExistsError(event=event, handler=handler)

        self.__subscribers[event].append(handler)
        logger.debug(f"Domain Event Handler '{handler.__class__.__name__}' is subscribed to '{event.__name__}' event")

    async def publish(self, event: DomainEvent) -> None:
        async with self.__unit_of_work:
            await self.__process_event(event)

    async def __process_event(self, event: DomainEvent) -> None:
        subscribers: List[DomainEventHandler] = self.__subscribers[type(event)]
        for subscriber in subscribers:
            logger.info(
                f"Event '{event.__class__.__name__} is being handled by '{subscriber.__class__.__name__}' handler"
            )
            try:
                await subscriber.handle(event.model_copy(deep=True))
            except Exception as e:
                logger.exception(f"An error occurred while processing '{event}' domain event: {str(e)}")
                raise EventualConsistencyError(error_detail=str(e)) from e
