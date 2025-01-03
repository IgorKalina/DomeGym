from dataclasses import dataclass

from src.shared_kernel.domain.exceptions import DomainError


@dataclass(kw_only=True, frozen=True)
class AppError(DomainError):
    @property
    def detail(self) -> str:
        return "Unknown application error has occurred"
