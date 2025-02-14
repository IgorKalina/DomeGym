from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class DataTransferObject(BaseModel):
    model_config = ConfigDict(extra="forbid")


class RepositoryDto(DataTransferObject):
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def __setattr__(self, name: str, value: Any) -> None:
        if name != "updated_at":
            super().__setattr__("updated_at", datetime.now(timezone.utc))
        super().__setattr__(name, value)
