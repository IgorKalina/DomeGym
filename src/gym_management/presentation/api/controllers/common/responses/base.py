from typing import Generic, Iterable, List, Optional, Protocol, TypeVar

from pydantic import BaseModel
from result import Result

from src.gym_management.domain.common.errors import Error
from src.gym_management.presentation.api.controllers.common.responses.mappers import map_error_type_to_http_status

from .orjson import ORJSONResponse

TError = TypeVar("TError")


class ResponseData(Protocol):
    def from_domain_model(self, data) -> "ResponseData":
        pass


class ErrorData(BaseModel, Generic[TError]):
    title: str = "Unknown error occurred"
    detail: TError | None = None


class OkResponse(BaseModel):
    status: int
    data: List


class ErrorResponse(BaseModel):
    status: int
    error: ErrorData


class Response:
    def __init__(self, status: int, response_data_model: Optional[ResponseData] = None) -> None:
        self._status = status
        self._response_data_model: Optional[ResponseData] = response_data_model

    def from_result(self, result: Result) -> ORJSONResponse:
        if result.is_err():
            return self._create_error_response(result)  # type: ignore
        return self._create_ok_response(result)

    @staticmethod
    def _create_error_response(result: Error) -> ORJSONResponse:
        status_code = map_error_type_to_http_status(result.get_error_type())
        error_detail = result.err()
        error_data: ErrorData = ErrorData(title=error_detail.title, detail=error_detail.description)
        error_response = ErrorResponse(
            status=status_code,
            error=error_data,
        )
        return ORJSONResponse(status_code=status_code, content=error_response)

    def _create_ok_response(self, result: Result) -> ORJSONResponse:
        if self._response_data_model is None:
            return self._empty_ok_response
        data = result.ok()
        if not data:
            return self._empty_ok_response
        if isinstance(data, Iterable):
            data = [self._response_data_model.from_domain_model(v) for v in data]
        else:
            data = [self._response_data_model.from_domain_model(data)]
        data = OkResponse(status=self._status, data=data)
        return ORJSONResponse(status_code=self._status, content=data)

    @property
    def _empty_ok_response(self) -> ORJSONResponse:
        return ORJSONResponse(
            status_code=self._status,
            content=OkResponse(status=self._status, data=[]),
        )
