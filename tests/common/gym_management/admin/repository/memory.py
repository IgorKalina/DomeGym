import uuid
from typing import List

from src.gym_management.application.common.dto.repository.admin import AdminDB
from src.gym_management.application.common.interfaces.repository.admin_repository import AdminRepository
from tests.common.gym_management.common.repository_state import RepositorySharedState


class AdminMemoryRepository(AdminRepository):
    def __init__(self, shared_state: RepositorySharedState) -> None:
        self.__shared_state = shared_state
        self.__admins: List[AdminDB] = self.__shared_state.admins

    async def create(self, admin: AdminDB) -> None:
        self.__admins.append(admin)

    async def get_by_id(self, admin_id: uuid.UUID) -> AdminDB | None:
        return next((adm for adm in self.__admins if adm.id == admin_id), None)

    async def get_multi(self) -> List[AdminDB]:
        return self.__admins.copy()

    async def update(self, admin: AdminDB) -> AdminDB:
        updated_admins = [adm for adm in self.__admins if adm.id != admin.id]
        updated_admins.append(admin)
        self.__admins = updated_admins
        return admin
