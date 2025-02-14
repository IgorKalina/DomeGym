import time
import uuid
from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field

__all__ = [
    "Entity",
]


class Entity(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def __setattr__(self, name: str, value: Any) -> None:
        if name != "updated_at":
            super().__setattr__("updated_at", datetime.now(timezone.utc))
        super().__setattr__(name, value)

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Entity):
            return False
        return self.id == other.id


if __name__ == "__main__":
    e = Entity()
    time.sleep(1)
    e.id = uuid.uuid4()
