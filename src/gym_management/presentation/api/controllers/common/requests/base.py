from uuid import UUID

from pydantic import BaseModel, field_serializer


class ApiRequest(BaseModel):
    @field_serializer("*")
    def serialize_uuid(self, uuid: UUID) -> str:
        return str(uuid)
