from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

__all__ = [
    "Entity",
]


@dataclass(kw_only=True)
class Entity(ABC):
    id: UUID = field(
        default_factory=uuid4,
    )
    created_at: datetime = field(
        default_factory=datetime.now,
    )

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Entity):
            return False
        return self.id == other.id
