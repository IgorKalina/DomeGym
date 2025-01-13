import uuid

from src.shared_kernel.application.dto import RepositoryDto


class AdminDB(RepositoryDto):
    id: uuid.UUID
    user_id: uuid.UUID
    subscription_id: uuid.UUID | None = None
