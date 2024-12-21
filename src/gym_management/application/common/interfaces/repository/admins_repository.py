import abc
import uuid
from typing import Optional

from src.gym_management.domain.admin.aggregate_root import Admin


class AdminsRepository(abc.ABC):
    @abc.abstractmethod
    async def create(self, admin: Admin) -> None:
        pass

    @abc.abstractmethod
    async def get_by_id(self, admin_id: uuid.UUID) -> Optional[Admin]:
        pass

    @abc.abstractmethod
    async def update(self, admin: Admin) -> Admin:
        pass
