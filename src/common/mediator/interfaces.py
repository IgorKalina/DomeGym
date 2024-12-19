from typing import Protocol, Type

from src.common.command import Command, CommandHandler, CommandResult, CommandType
from src.common.event import DomainEvent, DomainEventHandler, EventType
from src.common.query import Query, QueryHandler, QueryResult, QueryType


class BaseMediator(Protocol):
    pass


class ICommandMediator(BaseMediator, Protocol):
    async def send(self, command: Command) -> CommandResult:
        raise NotImplementedError

    def register_command_handler(
        self, command: Type[CommandType], handler: CommandHandler[CommandType, CommandResult]
    ) -> None:
        raise NotImplementedError


class IQueryMediator(BaseMediator, Protocol):
    async def query(self, query: Query) -> QueryResult:
        raise NotImplementedError

    def register_query_handler(self, query: Type[QueryType], handler: QueryHandler[QueryType, QueryResult]) -> None:
        raise NotImplementedError


class IEventMediator(BaseMediator, Protocol):
    async def publish(self, event: DomainEvent) -> None:
        raise NotImplementedError

    def register_event_handler(self, event: Type[EventType], handler: DomainEventHandler[EventType]) -> None:
        raise NotImplementedError


class IMediator(ICommandMediator, IQueryMediator, IEventMediator, BaseMediator, Protocol):
    pass
