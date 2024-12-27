import uuid
from typing import List, Optional

from src.gym_management.application.common.interfaces.repository.admins_repository import AdminsRepository
from src.gym_management.domain.admin.aggregate_root import Admin


class AdminsMemoryRepository(AdminsRepository):
    def __init__(self) -> None:
        self.__admins: List[Admin] = []

    async def create(self, admin: Admin) -> None:
        self.__admins.append(admin)

    async def get_by_id(self, admin_id: uuid.UUID) -> Optional[Admin]:
        return next((adm for adm in self.__admins if adm.id == admin_id), None)

    async def get_multi(self) -> List[Admin]:
        return self.__admins.copy()

    async def update(self, admin: Admin) -> Admin:
        updated_admins = [adm for adm in self.__admins if adm.id == admin.id]
        updated_admins.append(admin)
        self.__admins = updated_admins
        return admin
