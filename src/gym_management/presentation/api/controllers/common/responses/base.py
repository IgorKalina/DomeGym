from typing import Any, Generic, Iterable, List, Optional, Protocol, TypeVar

from fastapi import status
from pydantic import BaseModel, Field

from src.common.error_or import Error, ErrorOr
from src.gym_management.presentation.api.controllers.common.responses.mappers import map_error_type_to_http_status

from .orjson import ORJSONResponse

TError = TypeVar("TError")
TData = TypeVar("TData", bound=Any)


class ResponseData(Protocol):
    def from_domain_model(self, data) -> "ResponseData":
        pass


class ErrorData(BaseModel, Generic[TError]):
    title: str = "Unknown error occurred"
    detail: TError | None = None


class OkResponse(BaseModel, Generic[TData]):
    status: int = Field(examples=[status.HTTP_200_OK])
    data: List[TData]


class ErrorResponse(BaseModel):
    status: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    errors: List[ErrorData]


def create_response(result: ErrorOr, ok_status_code: int, response_data_model: Optional[ResponseData] = None):
    return ResultResponseAdapter(
        result=result,
        ok_status_code=ok_status_code,
        response_data_model=response_data_model,
    ).create_response()


class ResultResponseAdapter:
    def __init__(
        self,
        result: ErrorOr,
        ok_status_code: int,
        response_data_model: Optional[ResponseData] = None,
    ) -> None:
        self._ok_status_code = ok_status_code
        self._response_data_model: Optional[ResponseData] = response_data_model
        self._result: ErrorOr = result

    def create_response(self) -> ORJSONResponse:
        if self._result.is_error():
            return self._create_error_response()  # type: ignore
        return self._create_ok_response()

    def _create_error_response(self) -> ORJSONResponse:
        status_code = map_error_type_to_http_status(self._result.first_error.type)
        error_response = ErrorResponse(status=status_code, errors=self._map_errors_to_error_data(self._result.errors))
        return ORJSONResponse(media_type="application/problem+json", status_code=status_code, content=error_response)

    def _create_ok_response(self) -> ORJSONResponse:
        if self._response_data_model is None:
            return self._empty_ok_response
        data = self._result.value
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

    @staticmethod
    def _map_errors_to_error_data(errors: List[Error]) -> List[ErrorData]:
        errors_data: List[ErrorData] = []
        for error in errors:
            errors_data.append(ErrorData(title=error.code, detail=error.description))
        return errors_data
