import uuid

from sqlalchemy import select

from src.gym_management.application.common.interfaces.repository.admin_repository import AdminRepository
from src.gym_management.domain.admin.aggregate_root import Admin
from src.gym_management.infrastructure.db import models
from src.gym_management.infrastructure.db.mappers.admin import (
    map_admin_db_model_to_domain_model,
    map_admin_domain_model_to_db_model,
)
from src.gym_management.infrastructure.db.repository.sqlalchemy_repository import SQLAlchemyRepository


class AdminPostgresRepository(SQLAlchemyRepository, AdminRepository):
    async def create(self, admin: Admin) -> None:
        db_admin = map_admin_domain_model_to_db_model(admin)
        self._session.add(db_admin)
        await self._session.flush((db_admin,))
        await self._session.commit()

    async def get_by_id(self, admin_id: uuid.UUID) -> Admin | None:
        query = select(models.Admin).where(models.Admin.id == admin_id)
        result = await self._session.scalars(query)
        admin = result.one_or_none()
        return map_admin_db_model_to_domain_model(admin) if admin else None

    async def update(self, admin: Admin) -> Admin:
        db_admin = map_admin_domain_model_to_db_model(admin)
        await self._session.merge(db_admin)
        await self._session.flush((db_admin,))
        await self._session.commit()
        return map_admin_db_model_to_domain_model(db_admin)
