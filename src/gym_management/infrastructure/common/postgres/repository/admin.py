import uuid

from sqlalchemy import select

from src.gym_management.application.admin.exceptions import AdminDoesNotExistError
from src.gym_management.application.common.interfaces.repository.admin_repository import AdminRepository
from src.gym_management.domain.admin.aggregate_root import Admin
from src.gym_management.infrastructure.common.postgres import models
from src.gym_management.infrastructure.common.postgres.repository.sqlalchemy_repository import SQLAlchemyRepository


class AdminPostgresRepository(SQLAlchemyRepository, AdminRepository):
    async def create(self, admin: Admin) -> None:
        admin = models.Admin.from_domain(admin)
        self._session.add(admin)
        await self._session.flush((admin,))
        await self._session.commit()

    async def get(self, admin_id: uuid.UUID) -> Admin:
        admin: Admin | None = await self.get_or_none(admin_id)
        if admin is None:
            raise AdminDoesNotExistError()
        return admin

    async def get_or_none(self, admin_id: uuid.UUID) -> Admin | None:
        query = select(models.Admin).where(models.Admin.id == admin_id)
        result = await self._session.scalars(query)
        admin: models.Admin = result.one_or_none()
        return admin.to_domain() if admin else None

    async def update(self, admin: Admin) -> Admin:
        admin_db = await self._session.get(models.Admin, admin.id)
        if not admin_db:
            raise AdminDoesNotExistError()

        admin = models.Admin.from_domain(admin)
        await self._session.merge(admin)
        await self._session.commit()
        return admin.to_domain()
