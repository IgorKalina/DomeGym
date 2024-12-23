from dataclasses import dataclass

from src.shared_kernel.application.command import Command
from src.shared_kernel.application.event import DomainEvent
from src.shared_kernel.application.query.interfaces.query import Query


@dataclass(kw_only=True)
class HandlerNotFoundError(Exception):
    handlee: Command | Query | DomainEvent
    title: str = "Handler not found"

    @property
    def detail(self) -> str:
        return f"Handler for '{type(self.handlee).__name__}' was not registered"

    def __str__(self) -> str:
        return self.detail
