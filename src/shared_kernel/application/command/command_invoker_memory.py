from typing import Dict, Type

from src.shared_kernel.application.command.interfaces.command import Command, CommandHandler, CommandResult, CommandType
from src.shared_kernel.application.command.interfaces.command_invoker import CommandInvoker
from src.shared_kernel.application.mediator.exceptions import HandlerNotFoundError


class CommandInvokerMemory(CommandInvoker):
    def __init__(self) -> None:
        self.__command_handlers: Dict[Type[Command], CommandHandler] = {}

    def register_command_handler(
        self, command: Type[CommandType], handler: CommandHandler[CommandType, CommandResult]
    ) -> None:
        self.__command_handlers[command] = handler

    async def invoke(self, command: CommandType) -> CommandResult:
        handler = self.__command_handlers.get(type(command))
        if handler is None:
            raise HandlerNotFoundError(handlee=command)
        return await handler.handle(command)
