from typing import Any, List

from fastapi import status

from src.gym_management.presentation.api.controllers.common.responses.dto import (
    ErrorData,
    ErrorResponse,
    OkResponse,
    ResponseData,
)
from src.gym_management.presentation.api.controllers.common.responses.orjson import ORJSONResponse
from src.shared_kernel.application.error_or import Error, ErrorOr, ErrorType


class ErrorOrResponseAdapter:
    def __init__(
        self,
        result: ErrorOr | Any,
        ok_status_code: int,
        data: List[ResponseData],
    ) -> None:
        self._result: ErrorOr = result
        self._ok_status_code = ok_status_code
        self._data: List[ResponseData] = data

    def create_response(self) -> ORJSONResponse:
        if self._is_result_error_or():
            return self._create_response_from_error_or()
        return self._create_ok_response()

    def _create_response_from_error_or(self) -> ORJSONResponse:
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
        data: OkResponse = OkResponse(status=self._ok_status_code, data=self._data)
        return ORJSONResponse(status_code=self._ok_status_code, content=data)

    @property
    def _empty_ok_response(self) -> ORJSONResponse:
        return ORJSONResponse(
            status_code=self._ok_status_code,
            content=OkResponse(status=self._ok_status_code, data=[]),
        )

    @staticmethod
    def _map_errors_to_error_data(errors: List[Error]) -> List[ErrorData]:
        errors_data: List[ErrorData[Error]] = []
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

    def _is_result_error_or(self) -> bool:
        return isinstance(self._result, ErrorOr)
