import uuid

from src.gym_management.application.common.interfaces.repository.admin_repository import AdminRepository
from src.gym_management.domain.admin.aggregate_root import Admin
from src.shared_kernel.application.query.interfaces.query import Query, QueryHandler


class GetAdmin(Query):
    admin_id: uuid.UUID


class GetAdminHandler(QueryHandler):
    def __init__(self, admin_repository: AdminRepository) -> None:
        self.__admin_repository = admin_repository

    async def handle(self, query: GetAdmin) -> Admin:
        return await self.__admin_repository.get(query.admin_id)
