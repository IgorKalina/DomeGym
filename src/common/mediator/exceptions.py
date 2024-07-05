from dataclasses import dataclass

from src.common.command import Command
from src.common.event import DomainEvent
from src.common.query import Query


@dataclass
class MediatorException(Exception):
    title: str = "Unknown exception has occurred"

    @property
    def detail(self) -> str:
        return ""


@dataclass(kw_only=True)
class HandlerNotFoundException(MediatorException):
    handlee: Command | Query | DomainEvent
    title: str = "Handler not found"

    @property
    def detail(self) -> str:
        return f"Handler for '{type(self.handlee).__name__}' was not registered"
