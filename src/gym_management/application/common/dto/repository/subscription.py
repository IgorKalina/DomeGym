import uuid
from typing import List

from src.gym_management.domain.subscription.subscription_type import SubscriptionType
from src.shared_kernel.application.dto import RepositoryDto


class SubscriptionDB(RepositoryDto):
    id: uuid.UUID
    type: SubscriptionType
    admin_id: uuid.UUID
    gym_ids: List[uuid.UUID] = []
