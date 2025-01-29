import datetime

from pydantic import BaseModel, ConfigDict, Field


class DataTransferObject(BaseModel):
    model_config = ConfigDict(extra="forbid")


class RepositoryDto(DataTransferObject):
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
