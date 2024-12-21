from collections import defaultdict
from typing import Dict, List, Type

from src.shared_kernel.application.command import Command, CommandHandler, CommandResult, CommandType
from src.shared_kernel.application.event import DomainEvent, DomainEventHandler, EventType
from src.shared_kernel.application.mediator.exceptions import HandlerNotFoundError
from src.shared_kernel.application.mediator.interfaces import IMediator as MediatorInterface
from src.shared_kernel.application.mediator.interfaces import QueryResult, QueryType
from src.shared_kernel.application.query import Query, QueryHandler


class Mediator(MediatorInterface):
    def __init__(self) -> None:
        self.__command_handlers: Dict[Type[Command], CommandHandler] = {}
        self.__query_handlers: Dict[Type[Query], QueryHandler] = {}
        self.__event_handlers: Dict[Type[DomainEvent], List[DomainEventHandler]] = defaultdict(list)

    def register_command_handler(
        self, command: Type[CommandType], handler: CommandHandler[CommandType, CommandResult]
    ) -> None:
        self.__command_handlers[command] = handler

    def register_query_handler(self, query: Type[QueryType], handler: QueryHandler[QueryType, QueryResult]) -> None:
        self.__query_handlers[query] = handler

    def register_event_handler(self, event: Type[EventType], handler: DomainEventHandler[EventType]) -> None:
        self.__event_handlers[event].append(handler)

    async def send(self, command: Command) -> CommandResult:
        handler = self.__command_handlers.get(type(command))
        if handler is None:
            raise HandlerNotFoundError(handlee=command)
        return await handler.handle(command)

    async def query(self, query: Query) -> CommandResult:
        handler = self.__query_handlers.get(type(query))
        if handler is None:
            raise HandlerNotFoundError(handlee=query)
        return await handler.handle(query)

    async def publish(self, event: DomainEvent) -> None:
        handlers = self.__event_handlers.get(type(event), [])
        for handler in handlers:
            await handler.handle(event)
