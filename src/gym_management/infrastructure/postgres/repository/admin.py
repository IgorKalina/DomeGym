import uuid

from sqlalchemy import select

from src.gym_management.application.admin.exceptions import AdminDoesNotExistError
from src.gym_management.application.common.dto.repository.admin import AdminDB
from src.gym_management.application.common.interfaces.repository.admin_repository import AdminRepository
from src.gym_management.infrastructure.postgres import models
from src.gym_management.infrastructure.postgres.repository.sqlalchemy_repository import SQLAlchemyRepository


class AdminPostgresRepository(SQLAlchemyRepository, AdminRepository):
    async def create(self, admin: AdminDB) -> None:
        admin = models.Admin.from_dto(admin)
        self._session.add(admin)
        await self._session.flush((admin,))
        await self._session.commit()

    async def get_by_id(self, admin_id: uuid.UUID) -> AdminDB | None:
        query = select(models.Admin).where(models.Admin.id == admin_id)
        result = await self._session.scalars(query)
        admin: models.Admin = result.one_or_none()
        return admin.to_dto() if admin else None

    async def update(self, admin: AdminDB) -> AdminDB:
        admin_db = await self._session.get(models.Admin, admin.id)
        if not admin_db:
            raise AdminDoesNotExistError()

        admin = models.Admin.from_dto(admin)
        await self._session.merge(admin)
        await self._session.commit()
        return admin.to_dto()
