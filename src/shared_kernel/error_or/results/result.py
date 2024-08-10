from dataclasses import dataclass

from src.shared_kernel.error_or.results.result_type import ResultType


@dataclass(kw_only=True, frozen=True)
class Result:
    type: ResultType

    @classmethod
    def success(cls) -> "Result":
        return cls(type=ResultType.SUCCESS)

    @classmethod
    def created(cls) -> "Result":
        return cls(type=ResultType.CREATED)

    @classmethod
    def updated(cls) -> "Result":
        return cls(type=ResultType.UPDATED)

    @classmethod
    def deleted(cls) -> "Result":
        return cls(type=ResultType.DELETED)
