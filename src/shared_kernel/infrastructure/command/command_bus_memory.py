import logging
from typing import Dict, Type

from src.shared_kernel.application.command.interfaces.command import Command, CommandHandler, CommandResult, CommandType
from src.shared_kernel.application.command.interfaces.command_bus import CommandBus
from src.shared_kernel.application.exceptions import HandlerNotFoundError
from src.shared_kernel.infrastructure.interfaces.unit_of_work import UnitOfWork

logger = logging.getLogger(__name__)


class CommandBusMemory(CommandBus):
    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self.__unit_of_work = unit_of_work
        self.__command_handlers: Dict[Type[Command], CommandHandler] = {}

    async def invoke(self, command: CommandType) -> CommandResult:
        handler = self.__command_handlers.get(type(command))
        if handler is None:
            raise HandlerNotFoundError(handlee=command)
        logger.debug(f"Handling '{command.__class__.__name__}' command by '{handler.__class__.__name__}' handler")
        async with self.__unit_of_work:
            return await handler.handle(command)

    def register_command_handler(
        self, command: Type[CommandType], handler: CommandHandler[CommandType, CommandResult]
    ) -> None:
        self.__command_handlers[command] = handler
        logger.debug(f"Command Handler '{handler.__class__.__name__}' was registered for '{command.__name__}' command")
