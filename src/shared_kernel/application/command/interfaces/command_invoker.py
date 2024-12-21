import abc
from typing import Type

from .command import Command, CommandHandler, CommandResult, CommandType


class CommandInvoker(abc.ABC):
    @abc.abstractmethod
    async def invoke(self, command: Command) -> CommandResult:
        pass

    @abc.abstractmethod
    def register_command_handler(
        self, command: Type[CommandType], handler: CommandHandler[CommandType, CommandResult]
    ) -> None:
        pass
