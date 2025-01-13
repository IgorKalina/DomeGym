import abc
import uuid

from src.gym_management.application.admin.dto.repository import AdminDB


class AdminRepository(abc.ABC):
    @abc.abstractmethod
    async def create(self, admin: AdminDB) -> None:
        pass

    @abc.abstractmethod
    async def get_by_id(self, admin_id: uuid.UUID) -> AdminDB | None:
        pass

    @abc.abstractmethod
    async def update(self, admin: AdminDB) -> AdminDB:
        pass
