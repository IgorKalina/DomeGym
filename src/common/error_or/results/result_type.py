from enum import Enum, auto


class ResultType(Enum):
    SUCCESS = auto()
    CREATED = auto()
    UPDATED = auto()
    DELETED = auto()
