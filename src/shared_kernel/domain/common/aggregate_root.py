from copy import copy
from typing import List

from pydantic import PrivateAttr

from src.shared_kernel.domain.common.entity import Entity
from src.shared_kernel.domain.common.event import DomainEvent


class AggregateRoot(Entity):
    _domain_events: List[DomainEvent] = PrivateAttr(default_factory=list)

    def pop_domain_events(self) -> List[DomainEvent]:
        registered_events = copy(self._domain_events)
        self._domain_events.clear()
        return registered_events

    def _create_domain_event(self, event: DomainEvent) -> None:
        self._domain_events.append(event)
