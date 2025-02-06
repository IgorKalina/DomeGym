import logging
from typing import List

import jsonpickle
from tinydb import TinyDB

from src.shared_kernel.application.event.domain.repository import FailedDomainEventRepository
from src.shared_kernel.domain.common.event import DomainEvent

logger = logging.getLogger(__name__)


class FailedDomainEventTinyDBRepository(FailedDomainEventRepository):
    def __init__(self) -> None:
        self.__db_path: str = "domain_events.json"
        self.__db = TinyDB(self.__db_path)
        self.__table = self.__db.table("failed_events")

    async def create(self, event: DomainEvent) -> DomainEvent:
        data = {"type": event.__class__.__name__, "data": jsonpickle.encode(event)}
        self.__table.insert(data)
        return event

    async def get_multi(self) -> List[DomainEvent]:
        # Retrieve all the events from TinyDB
        stored_events = self.__table.all()
        domain_events: List[DomainEvent] = [jsonpickle.decode(event["data"]) for event in stored_events]  # noqa: S301, possibly security issue to solve
        return domain_events

    async def truncate(self) -> None:
        self.__table.truncate()
