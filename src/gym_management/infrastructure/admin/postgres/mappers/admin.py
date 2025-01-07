from src.gym_management.domain.admin.aggregate_root import Admin

from .. import models


def map_admin_domain_model_to_db_model(admin: Admin) -> models.Admin:
    return models.Admin(
        id=admin.id,
        user_id=admin.user_id,
    )


def map_admin_db_model_to_domain_model(admin: models.Admin) -> Admin:
    return Admin(
        id=admin.id,
        user_id=admin.user_id,
    )
