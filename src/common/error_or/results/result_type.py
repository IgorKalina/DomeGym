from enum import StrEnum, auto


class ResultType(StrEnum):
    SUCCESS = auto()
    CREATED = auto()
    UPDATED = auto()
    DELETED = auto()
