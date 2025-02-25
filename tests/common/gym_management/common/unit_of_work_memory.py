from typing import Self, Type

from src.shared_kernel.infrastructure.interfaces.unit_of_work import UnitOfWork


class UnitOfWorkMemory(UnitOfWork):
    async def commit(self) -> None:
        pass

    async def rollback(self) -> None:
        pass

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self, exc_type: Type[BaseException] | None, exc_value: BaseException | None, traceback: str
    ) -> None:
        pass
