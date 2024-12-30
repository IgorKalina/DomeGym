import datetime
import uuid

from pydantic import Field

from src.gym_management.presentation.api.controllers.common.responses.dto import ResponseData


class GymResponse(ResponseData):
    id: uuid.UUID
    subscription_id: uuid.UUID
    name: str = Field(examples=["MyGym"])
    created_at: datetime.datetime
