import abc
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

__all__ = [
    "Query",
    "QueryHandler",
    "QueryType",
    "QueryResult",
]

query_dataclass = dataclass(frozen=True)


@query_dataclass
class Query(abc.ABC):
    pass


QueryType = TypeVar("QueryType", bound=Query)
QueryResult = TypeVar("QueryResult", bound=Any)


class QueryHandler(abc.ABC, Generic[QueryType, QueryResult]):
    @abc.abstractmethod
    async def handle(self, query: QueryType) -> QueryResult:
        pass
