import abc
import dataclasses
from typing import Any, Generic, TypeVar

__all__ = ["Command", "CommandHandler", "CommandType", "CommandResult"]


@dataclasses.dataclass(kw_only=True, frozen=True)
class Command(abc.ABC):
    pass


CommandType = TypeVar("CommandType", bound=Command)
CommandResult = TypeVar("CommandResult", bound=Any)


class CommandHandler(abc.ABC, Generic[CommandType, CommandResult]):
    @abc.abstractmethod
    async def handle(self, command: CommandType) -> CommandResult:
        pass
