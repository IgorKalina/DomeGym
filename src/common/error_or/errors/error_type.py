from enum import Enum, auto


class ErrorType(Enum):
    FAILURE = auto()
    UNEXPECTED = auto()
    VALIDATION = auto()
    CONFLICT = auto()
    NOT_FOUND = auto()
    UNAUTHORIZED = auto()
    FORBIDDEN = auto()
