from src.gym_management.application.common.dto.repository.subscription import SubscriptionDB
from src.gym_management.domain.subscription.aggregate_root import Subscription


def db_to_domain(subscription: SubscriptionDB) -> Subscription:
    return Subscription(
        id=subscription.id,
        type=subscription.type,
        admin_id=subscription.admin_id,
        gym_ids=subscription.gym_ids,
        created_at=subscription.created_at,
        updated_at=subscription.updated_at,
    )


def domain_to_db(subscription: Subscription) -> SubscriptionDB:
    return SubscriptionDB(
        id=subscription.id,
        type=subscription.type,
        admin_id=subscription.admin_id,
        created_at=subscription.created_at,
        updated_at=subscription.updated_at,
    )
