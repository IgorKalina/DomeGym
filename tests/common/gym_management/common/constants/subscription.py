import uuid

from src.gym_management.domain.subscription.subscription_type import SubscriptionType

SUBSCRIPTION_ID = uuid.UUID("f7805f92-12ca-4dd5-8f23-5f965f325ca5")
DEFAULT_SUBSCRIPTION_TYPE = SubscriptionType.FREE

MAX_SESSIONS_FREE_TIER = 3
MAX_ROOMS_FREE_TIER = 1
MAX_GYMS_FREE_TIER = 1
