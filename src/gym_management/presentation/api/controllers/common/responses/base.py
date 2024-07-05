from typing import Generic, Iterable, List, Optional, Protocol, TypeVar

from fastapi import status
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
    status: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    errors: List[ErrorData]


class ResultResponseAdapter:
    def __init__(
        self,
        result: Result,
        ok_status_code: int,
        response_data_model: Optional[ResponseData] = None,
    ) -> None:
        self._ok_status_code = ok_status_code
        self._response_data_model: Optional[ResponseData] = response_data_model
        self._result: Result | Error = result

    def create_response(self) -> ORJSONResponse:
        if self._result.is_err():
            return self._create_error_response()  # type: ignore
        return self._create_ok_response()

    def _create_error_response(self) -> ORJSONResponse:
        status_code = map_error_type_to_http_status(self._result.get_error_type())
        error_detail = self._result.err()
        error_data: ErrorData = ErrorData(title=error_detail.title, detail=error_detail.description)
        error_response = ErrorResponse(
            status=status_code,
            errors=[error_data],  # todo: add support for multiple errors
        )
        return ORJSONResponse(media_type="application/problem+json", status_code=status_code, content=error_response)

    def _create_ok_response(self) -> ORJSONResponse:
        if self._response_data_model is None:
            return self._empty_ok_response
        data = self._result.ok()
        if not data:
            return self._empty_ok_response
        if isinstance(data, Iterable):
            data = [self._response_data_model.from_domain_model(v) for v in data]
        else:
            data = [self._response_data_model.from_domain_model(data)]
        data = OkResponse(status=self._ok_status_code, data=data)
        return ORJSONResponse(status_code=self._ok_status_code, content=data)

    @property
    def _empty_ok_response(self) -> ORJSONResponse:
        return ORJSONResponse(
            status_code=self._ok_status_code,
            content=OkResponse(status=self._ok_status_code, data=[]),
        )
