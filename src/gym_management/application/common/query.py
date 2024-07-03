import abc
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

__all__ = [
    "Query",
    "QueryHandler",
]


@dataclass(frozen=True)
class Query(abc.ABC):
    pass


QT = TypeVar("QT", bound=Query)
QR = TypeVar("QR", bound=Any)


class QueryHandler(abc.ABC, Generic[QT, QR]):
    @abc.abstractmethod
    async def handle(self, query: QT) -> QR:
        pass
