from typing import Any, Generic, List, TypeVar

from fastapi import status
from pydantic import BaseModel, Field


class ResponseData(BaseModel):
    pass


ErrorType = TypeVar("ErrorType", bound=Any)
DataType = TypeVar("DataType", bound=ResponseData)


class ErrorData(BaseModel, Generic[ErrorType]):
    title: str
    detail: str


class Response(BaseModel):
    status: int
    data: List
    errors: List


class OkResponse(Response, Generic[DataType]):
    status: int = Field(examples=[status.HTTP_200_OK])
    data: List[DataType]
    errors: List = []


class ErrorResponse(Response, Generic[ErrorType]):
    status: int = Field(examples=[status.HTTP_400_BAD_REQUEST])
    errors: List[ErrorData[ErrorType]]
    data: List = []
