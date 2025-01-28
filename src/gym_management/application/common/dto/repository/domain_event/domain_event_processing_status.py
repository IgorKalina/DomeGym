from enum import StrEnum, auto


class DomainEventProcessingStatus(StrEnum):
    PENDING = auto()
    PUBLISHED = auto()
    PROCESSED = auto()
    FAILED = auto()
