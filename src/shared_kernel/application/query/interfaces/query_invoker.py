import abc
from typing import Type

from .query import Query, QueryHandler, QueryResult, QueryType


class QueryInvoker(abc.ABC):
    @abc.abstractmethod
    async def invoke(self, query: Query) -> QueryResult:
        pass

    @abc.abstractmethod
    def register_query_handler(self, query: Type[QueryType], handler: QueryHandler[QueryType, QueryResult]) -> None:
        pass
