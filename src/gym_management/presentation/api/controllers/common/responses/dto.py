from typing import Any, Generic, List, TypeVar

from fastapi import status
from pydantic import BaseModel, Field

TError = TypeVar("TError", bound=Any)
TData = TypeVar("TData", bound=BaseModel)


class ErrorData(BaseModel, Generic[TError]):
    title: str = "Unknown error occurred"
    detail: str


class Response(BaseModel):
    status: int = Field(examples=[status.HTTP_200_OK])
    data: List
    errors: List


class OkResponse(Response, Generic[TData]):
    data: List[TData]
    errors: List = []


class ErrorResponse(Response, Generic[TError]):
    errors: List[ErrorData[TError]]
    data: List = []
