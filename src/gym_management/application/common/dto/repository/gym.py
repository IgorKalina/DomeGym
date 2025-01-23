import uuid
from typing import List

from src.shared_kernel.application.dto import RepositoryDto


class GymDB(RepositoryDto):
    id: uuid.UUID
    name: str
    subscription_id: uuid.UUID
    room_ids: List[uuid.UUID] = []
