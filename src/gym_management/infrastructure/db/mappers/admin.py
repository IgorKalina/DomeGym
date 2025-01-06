from src.gym_management.domain.admin.aggregate_root import Admin
from src.gym_management.infrastructure.db import models


def map_admin_domain_model_to_db_model(admin: Admin) -> models.Gym:
    return models.Admin(
        id=admin.id,
        user_id=admin.user_id,
    )


def map_admin_db_model_to_domain_model(admin: models.Admin) -> Admin:
    return Admin(
        id=admin.id,
        user_id=admin.user_id,
    )
