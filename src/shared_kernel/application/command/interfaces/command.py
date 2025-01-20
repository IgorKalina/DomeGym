import abc
from typing import Any, Generic, TypeVar

from pydantic import BaseModel

__all__ = ["Command", "CommandHandler", "CommandType", "CommandResult"]


class Command(BaseModel):
    pass


CommandType = TypeVar("CommandType", bound=Command)
CommandResult = TypeVar("CommandResult", bound=Any)


class CommandHandler(abc.ABC, Generic[CommandType, CommandResult]):
    @abc.abstractmethod
    async def handle(self, command: CommandType) -> CommandResult:
        pass
