import dataclasses
import json
import logging
from typing import Dict, List, Type

from tinydb import TinyDB

from src.shared_kernel.application.event.domain.repository import FailedDomainEventRepository
from src.shared_kernel.domain.event import DomainEvent

logger = logging.getLogger(__name__)


class FailedDomainEventTinyDBRepository(FailedDomainEventRepository):
    def __init__(self) -> None:
        self.__db_path: str = "domain_events.json"
        self.__db = TinyDB(self.__db_path)
        self.__table = self.__db.table("failed_events")

    async def create(self, event: DomainEvent) -> DomainEvent:
        data = {"type": event.__class__.__name__, "data": json.dumps(dataclasses.asdict(event))}
        self.__table.insert(data)
        return event

    async def get_multi(self) -> List[DomainEvent]:
        # Retrieve all the events from TinyDB
        stored_events = self.__table.all()
        domain_events: List[DomainEvent] = [self.__map_raw_event_to_domain_event(event) for event in stored_events]
        self.__table.truncate()
        return domain_events

    def __map_raw_event_to_domain_event(self, event: Dict) -> DomainEvent:
        event_type = event.pop("type")
        event_raw: Dict = json.loads(event["data"])
        domain_event_class: Type[DomainEvent] | None = self.__get_event_class_by_type(event_type)
        if domain_event_class is None:
            raise TypeError(f"Type for '{event_type}' event type does not exist")
        return domain_event_class(**event_raw)

    @staticmethod
    def __get_event_class_by_type(event_type: str) -> Type[DomainEvent] | None:
        """
        Dynamically find and return the class based on event type
        """
        # Check for subclasses of DomainEvent
        subclasses = DomainEvent.__subclasses__()
        for subclass in subclasses:
            if subclass.__name__ == event_type:
                return subclass
            # Recursively check subclasses of subclasses
            subclass_subclasses = subclass.__subclasses__()
            for sub_subclass in subclass_subclasses:
                if sub_subclass.__name__ == event_type:
                    return sub_subclass
        return None
