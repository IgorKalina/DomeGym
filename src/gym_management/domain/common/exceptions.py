from dataclasses import dataclass

from src.shared_kernel.application.error_or import ErrorType


@dataclass(kw_only=True)
class DomainError(Exception):
    entity_name: str = "Unknown"
    error_type: ErrorType = ErrorType.UNEXPECTED

    @property
    def title(self) -> str:
        return f"{self.entity_name.capitalize()}.{self.error_type.name.capitalize()}"

    @property
    def detail(self) -> str:
        return "Unknown domain error has occurred"

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(title='{self.title}', detail='{self.detail}')"
