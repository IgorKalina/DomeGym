import uuid

from src.shared_kernel.application.dto import RepositoryDto


class RoomDB(RepositoryDto):
    id: uuid.UUID
    name: str
    gym_id: uuid.UUID
    subscription_id: uuid.UUID
