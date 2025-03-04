import abc
from abc import abstractmethod
from typing import Any, Generic, List, TypeVar

from pydantic import BaseModel, Field

from src.gym_management.presentation.api.controllers.common.responses.orjson import ORJSONResponse


class ResponseData(BaseModel):
    pass


ErrorType = TypeVar("ErrorType", bound=Any)
DataType = TypeVar("DataType", bound=ResponseData)


class ErrorData(BaseModel, Generic[ErrorType]):
    title: str
    detail: str


class Response(abc.ABC, BaseModel):
    status: int = Field(exclude=True)
    data: List
    errors: List

    @abstractmethod
    def to_orjson(self) -> ORJSONResponse:
        pass


class OkResponse(Response, Generic[DataType]):
    data: List[DataType] = []
    errors: List = []

    def to_orjson(self) -> ORJSONResponse:
        return ORJSONResponse(status_code=self.status, content=self)


class ErrorResponse(Response, Generic[ErrorType]):
    errors: List[ErrorData[ErrorType]]
    data: List = []

    def to_orjson(self) -> ORJSONResponse:
        return ORJSONResponse(media_type="application/problem+json", status_code=self.status, content=self)
