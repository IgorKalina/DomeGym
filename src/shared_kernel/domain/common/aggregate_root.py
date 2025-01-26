from copy import copy
from dataclasses import dataclass, field
from typing import List

from src.shared_kernel.domain.common.entity import Entity
from src.shared_kernel.domain.common.event import DomainEvent


@dataclass(kw_only=True)
class AggregateRoot(Entity):
    _domain_events: List[DomainEvent] = field(default_factory=list, init=False, repr=False)

    def pop_domain_events(self) -> List[DomainEvent]:
        registered_events = copy(self._domain_events)
        self._domain_events.clear()
        return registered_events

    def _create_domain_event(self, event: DomainEvent) -> None:
        self._domain_events.append(event)
