import uuid

from src.gym_management.application.admin.exceptions import AdminDoesNotExistError
from src.gym_management.application.common.dto.repository import AdminDB, SubscriptionDB
from src.gym_management.application.common.interfaces.repository.admin_repository import AdminRepository
from src.shared_kernel.application.query.interfaces.query import Query, QueryHandler


class GetAdmin(Query):
    admin_id: uuid.UUID


class GetAdminHandler(QueryHandler):
    def __init__(self, admin_repository: AdminRepository) -> None:
        self.__admin_repository = admin_repository

    async def handle(self, query: GetAdmin) -> SubscriptionDB:
        admin_db: AdminDB | None = await self.__admin_repository.get_by_id(query.admin_id)
        if admin_db is None:
            raise AdminDoesNotExistError()
        return admin_db
