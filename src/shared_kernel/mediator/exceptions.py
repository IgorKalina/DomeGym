from dataclasses import dataclass

from src.shared_kernel.command import Command
from src.shared_kernel.event import DomainEvent
from src.shared_kernel.query import Query


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

    def __str__(self) -> str:
        return self.detail
