from enum import StrEnum


class DomainEventProcessingStatus(StrEnum):
    PENDING = "PENDING"
    PUBLISHED = "PUBLISHED"
    PROCESSED = "PROCESSED"
    FAILED = "FAILED"
