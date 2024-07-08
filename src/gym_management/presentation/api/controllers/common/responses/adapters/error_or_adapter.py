from typing import Iterable, List, Optional, Protocol

from fastapi import status

from src.common.error_or import Error, ErrorOr, ErrorType
from src.gym_management.presentation.api.controllers.common.responses.orjson import ORJSONResponse
from src.gym_management.presentation.api.controllers.common.responses.schema import ErrorData, ErrorResponse, OkResponse


class ResponseData(Protocol):
    def from_domain_model(self, data) -> "ResponseData":
        pass


class ErrorOrResponseAdapter:
    def __init__(
        self,
        result: ErrorOr,
        ok_status_code: int,
        response_data_model: Optional[ResponseData] = None,
    ) -> None:
        self._result: ErrorOr = result
        self._ok_status_code = ok_status_code
        self._response_data_model: Optional[ResponseData] = response_data_model

    def create_response(self) -> ORJSONResponse:
        if self._result.is_error():
            return self._create_error_response()  # type: ignore
        return self._create_ok_response()

    def _create_error_response(self) -> ORJSONResponse:
        error_status_code: int = self._map_error_type_to_http_status(self._result.first_error.type)
        error_response: ErrorResponse = ErrorResponse(
            status=error_status_code, errors=self._map_errors_to_error_data(self._result.errors)
        )
        return ORJSONResponse(
            media_type="application/problem+json", status_code=error_status_code, content=error_response
        )

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

    @staticmethod
    def _map_error_type_to_http_status(error_type: ErrorType) -> int:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        match error_type:
            case ErrorType.FAILURE:
                status_code = status.HTTP_400_BAD_REQUEST
            case ErrorType.UNEXPECTED:
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            case ErrorType.VALIDATION:
                status_code = status.HTTP_400_BAD_REQUEST
            case ErrorType.CONFLICT:
                status_code = status.HTTP_409_CONFLICT
            case ErrorType.NOT_FOUND:
                status_code = status.HTTP_404_NOT_FOUND
            case ErrorType.UNAUTHORIZED:
                status_code = status.HTTP_401_UNAUTHORIZED
            case ErrorType.FORBIDDEN:
                status_code = status.HTTP_403_FORBIDDEN
        return status_code
