import abc
import uuid

from src.gym_management.domain.admin.aggregate_root import Admin


class AdminRepository(abc.ABC):
    @abc.abstractmethod
    async def create(self, admin: Admin) -> None:
        pass

    @abc.abstractmethod
    async def get(self, admin_id: uuid.UUID) -> Admin:
        pass

    @abc.abstractmethod
    async def get_or_none(self, admin_id: uuid.UUID) -> Admin | None:
        pass

    @abc.abstractmethod
    async def update(self, admin: Admin) -> Admin:
        pass
