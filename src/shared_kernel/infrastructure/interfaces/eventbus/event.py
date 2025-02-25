import uuid

from src.shared_kernel.application.dto import DataTransferObject


class Event(DataTransferObject):
    id: uuid.UUID
    data: dict
    event_type: str
