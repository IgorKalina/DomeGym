import abc
from typing import Self, Type


class UnitOfWork(abc.ABC):
    @abc.abstractmethod
    async def commit(self) -> None:
        pass

    @abc.abstractmethod
    async def rollback(self) -> None:
        pass

    @abc.abstractmethod
    async def __aenter__(self) -> Self:
        pass

    @abc.abstractmethod
    async def __aexit__(
        self, exc_type: Type[BaseException] | None, exc_value: BaseException | None, traceback: str
    ) -> None:
        pass
