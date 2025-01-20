import abc
from typing import Any, Generic, TypeVar

from pydantic import BaseModel

__all__ = [
    "Query",
    "QueryHandler",
    "QueryType",
    "QueryResult",
]


class Query(BaseModel):
    pass


QueryType = TypeVar("QueryType", bound=Query)
QueryResult = TypeVar("QueryResult", bound=Any)


class QueryHandler(abc.ABC, Generic[QueryType, QueryResult]):
    @abc.abstractmethod
    async def handle(self, query: QueryType) -> QueryResult:
        pass
