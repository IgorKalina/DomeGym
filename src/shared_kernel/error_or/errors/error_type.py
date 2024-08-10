from enum import StrEnum, auto


class ErrorType(StrEnum):
    FAILURE = auto()
    UNEXPECTED = auto()
    VALIDATION = auto()
    CONFLICT = auto()
    NOT_FOUND = auto()
    UNAUTHORIZED = auto()
    FORBIDDEN = auto()
