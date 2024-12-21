from dataclasses import dataclass

from src.shared_kernel.application.command import Command
from src.shared_kernel.application.event import DomainEvent
from src.shared_kernel.application.query import Query


@dataclass
class MediatorError(Exception):
    title: str = "Unknown exception has occurred"

    @property
    def detail(self) -> str:
        return ""


@dataclass(kw_only=True)
class HandlerNotFoundError(MediatorError):
    handlee: Command | Query | DomainEvent
    title: str = "Handler not found"

    @property
    def detail(self) -> str:
        return f"Handler for '{type(self.handlee).__name__}' was not registered"

    def __str__(self) -> str:
        return self.detail
