from src.gym_management.application.common.dto.repository import AdminDB
from src.gym_management.domain.admin.aggregate_root import Admin


def db_to_domain(admin: AdminDB) -> Admin:
    return Admin(id=admin.id, user_id=admin.user_id, subscription_id=admin.subscription_id, created_at=admin.created_at)


def domain_to_db(admin: Admin) -> AdminDB:
    return AdminDB(
        id=admin.id, user_id=admin.user_id, subscription_id=admin.subscription_id, created_at=admin.created_at
    )
