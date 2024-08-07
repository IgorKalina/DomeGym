from typing import Any, Generic, List, TypeVar

from fastapi import status
from pydantic import BaseModel, Field

TError = TypeVar("TError")
TData = TypeVar("TData", bound=Any)


class Response(BaseModel):
    pass


class ErrorData(BaseModel, Generic[TError]):
    title: str = "Unknown error occurred"
    detail: TError | None = None


class OkResponse(Response, Generic[TData]):
    status: int = Field(examples=[status.HTTP_200_OK])
    data: List[TData]


class ErrorResponse(Response, Generic[TError]):
    status: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    errors: List[ErrorData]
