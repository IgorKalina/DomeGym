import uuid
from typing import List

from src.gym_management.application.admin.exceptions import AdminDoesNotExistError
from src.gym_management.application.common.interfaces.repository.admin_repository import AdminRepository
from src.gym_management.domain.admin.aggregate_root import Admin
from tests.common.gym_management.common.repository_state import RepositorySharedState


class AdminMemoryRepository(AdminRepository):
    def __init__(self, shared_state: RepositorySharedState) -> None:
        self.__shared_state = shared_state
        self.__admins: List[Admin] = self.__shared_state.admins

    async def create(self, admin: Admin) -> None:
        self.__admins.append(admin)

    async def get(self, admin_id: uuid.UUID) -> Admin:
        admin: Admin | None = await self.get_or_none(admin_id)
        if admin is None:
            raise AdminDoesNotExistError()
        return admin

    async def get_or_none(self, admin_id: uuid.UUID) -> Admin | None:
        return next((adm for adm in self.__admins if adm.id == admin_id), None)

    async def update(self, admin: Admin) -> Admin:
        updated_admins = [adm for adm in self.__admins if adm.id != admin.id]
        updated_admins.append(admin)
        self.__admins = updated_admins
        return admin
