import datetime
import uuid

from pydantic import Field

from src.gym_management.presentation.api.controllers.common.responses.dto import ResponseData


class RoomResponse(ResponseData):
    id: uuid.UUID
    name: str = Field(examples=["MyRoom"])
    gym_id: uuid.UUID
    subscription_id: uuid.UUID
    created_at: datetime.datetime
