from typing import Generic, TypeVar

from fastapi import status
from pydantic import BaseModel, Field

TResult = TypeVar("TResult")
TError = TypeVar("TError")


class Response(BaseModel):
    class Config:
        arbitrary_types_allowed = True


class OkResponse(Response, Generic[TResult]):
    status: int = status.HTTP_200_OK
    result: TResult | None = None


class ErrorData(BaseModel, Generic[TError]):
    title: str = "Unknown error occurred"
    data: TError | None = None


class ErrorResponse(Response, Generic[TError]):
    status: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    error: ErrorData[TError] = Field(default_factory=ErrorData)
