from src.gym_management.application.common.dto.repository import AdminDB
from src.gym_management.domain.admin.aggregate_root import Admin


def map_admin_dto_to_domain(admin: AdminDB) -> Admin:
    return Admin(id=admin.id, user_id=admin.user_id, subscription_id=admin.subscription_id, created_at=admin.created_at)


def map_admin_domain_to_db_dto(admin: Admin) -> AdminDB:
    return AdminDB(
        id=admin.id, user_id=admin.user_id, subscription_id=admin.subscription_id, created_at=admin.created_at
    )
