from dataclasses import dataclass
from typing import Type

from src.shared_kernel.application.command import Command
from src.shared_kernel.application.query.interfaces.query import Query
from src.shared_kernel.domain.event import DomainEvent, DomainEventHandler


@dataclass(kw_only=True, frozen=True)
class AppError(Exception):
    title: str

    @property
    def detail(self) -> str:
        return "Unknown application error has occurred"

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(title='{self.title}', detail='{self.detail}')"


@dataclass(kw_only=True, frozen=True)
class HandlerNotFoundError(AppError):
    handlee: Command | Query
    title: str = "Handler not found"

    @property
    def detail(self) -> str:
        return f"Handler for '{type(self.handlee).__name__}' was not registered"


@dataclass(kw_only=True, frozen=True)
class EventHandlerAlreadyExistsError(AppError):
    event: Type[DomainEvent]
    handler: DomainEventHandler
    title: str = "Handler already exists"

    @property
    def detail(self) -> str:
        return f"Handler '{self.handler.__class__.__name__}' for '{type(self.event).__name__}' event already exists"
