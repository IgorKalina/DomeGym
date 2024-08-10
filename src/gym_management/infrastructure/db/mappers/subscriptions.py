from src.gym_management.domain.subscription.aggregate_root import Subscription
from src.gym_management.infrastructure.db import models


def map_subscription_domain_model_to_db_model(subscription: Subscription) -> models.Subscription:
    return models.Subscription(
        id=subscription.id,
        type=subscription.type,
        admin_id=subscription.admin_id,
    )


def map_subscription_db_model_to_domain_model(subscription: models.Subscription) -> Subscription:
    return Subscription(
        id=subscription.id,
        subscription_type=subscription.type,
        admin_id=subscription.admin_id,
    )
