import abc
from abc import abstractmethod
from typing import List

from src.shared_kernel.domain.event import DomainEvent


class FailedDomainEventRepository(abc.ABC):
    @abstractmethod
    async def create(self, event: DomainEvent) -> DomainEvent:
        pass

    @abstractmethod
    async def get_multi(self) -> List[DomainEvent]:
        pass

    @abstractmethod
    async def truncate(self) -> None:
        pass
