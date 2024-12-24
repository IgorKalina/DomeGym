from typing import Any
from uuid import UUID

from pydantic import BaseModel, field_serializer


class ApiRequest(BaseModel):
    @field_serializer("*", when_used="unless-none")
    def serialize_uuid(self, value: Any) -> str:
        if isinstance(value, UUID):
            return str(value)
        return value
