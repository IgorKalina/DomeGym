import logging
from typing import Self, Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.shared_kernel.infrastructure.interfaces.unit_of_work import UnitOfWork

logger = logging.getLogger(__name__)


class SQLAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session: AsyncSession) -> None:
        self.__session: AsyncSession = session

    @property
    def session(self) -> AsyncSession:
        return self.__session

    async def commit(self) -> None:
        await self.__session.commit()

    async def rollback(self) -> None:
        await self.__session.rollback()

    async def __aenter__(self) -> Self:
        await self.__session.begin_nested()
        return self

    async def __aexit__(
        self, exc_type: Type[BaseException] | None, exc_value: BaseException | None, traceback: str
    ) -> None:
        if exc_type:
            await self.rollback()
            logger.debug("SQLAlchemy session has been rolled back")
        else:
            await self.commit()
            logger.debug("SQLAlchemy session has been committed")
        await self.__session.reset()
        logger.debug("SQLAlchemy session has been closed")
