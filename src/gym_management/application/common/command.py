import abc
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

__all__ = [
    "Command",
    "CommandHandler",
]


@dataclass(frozen=True)
class Command(abc.ABC):
    pass


CT = TypeVar("CT", bound=Command)
CR = TypeVar("CR", bound=Any)


class CommandHandler(abc.ABC, Generic[CT, CR]):
    @abc.abstractmethod
    async def handle(self, command: CT) -> CR:
        pass
