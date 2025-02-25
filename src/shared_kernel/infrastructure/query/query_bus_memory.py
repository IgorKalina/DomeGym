import logging
from typing import Dict, Type

from src.shared_kernel.application.exceptions import HandlerNotFoundError
from src.shared_kernel.application.query.interfaces.query import Query, QueryHandler, QueryResult, QueryType
from src.shared_kernel.application.query.interfaces.query_bus import QueryBus
from src.shared_kernel.infrastructure.interfaces.unit_of_work import UnitOfWork

logger = logging.getLogger(__name__)


class QueryBusMemory(QueryBus):
    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self.__unit_of_work: UnitOfWork = unit_of_work
        self.__query_handlers: Dict[Type[Query], QueryHandler] = {}

    async def invoke(self, query: Query) -> QueryResult:
        handler = self.__query_handlers.get(type(query))
        if handler is None:
            raise HandlerNotFoundError(handlee=query)
        logger.debug(f"Handling '{query.__class__.__name__}' query by '{handler.__class__.__name__}' handler")
        async with self.__unit_of_work:
            return await handler.handle(query)

    def register_query_handler(self, query: Type[QueryType], handler: QueryHandler[QueryType, QueryResult]) -> None:
        self.__query_handlers[query] = handler
        logger.debug(f"Query Handler '{handler.__class__.__name__}' was registered for '{query.__name__}' query")
