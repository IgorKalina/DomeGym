import datetime

from pydantic import BaseModel, Field


class DataTransferObject(BaseModel):
    pass


class RepositoryDto(DataTransferObject):
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
