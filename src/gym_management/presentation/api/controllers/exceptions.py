import logging
from urllib.request import Request

from fastapi import FastAPI, status

from src.gym_management.domain.common.exceptions import DomainError
from src.gym_management.presentation.api.controllers.common.responses.dto import ErrorData, ErrorResponse
from src.gym_management.presentation.api.controllers.common.responses.orjson import ORJSONResponse
from src.shared_kernel.application.error_or import ErrorType

logger = logging.getLogger(__name__)


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(DomainError, domain_exception_handler)
    app.add_exception_handler(Exception, unknown_exception_handler)


async def domain_exception_handler(request: Request, err: DomainError) -> ORJSONResponse:  # noqa: ARG001
    logger.error("Handling error", exc_info=err, extra={"error": err})
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    match err.error_type:
        case ErrorType.FAILURE:
            status_code = status.HTTP_400_BAD_REQUEST
        case ErrorType.UNEXPECTED:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        case ErrorType.VALIDATION:
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        case ErrorType.CONFLICT:
            status_code = status.HTTP_409_CONFLICT
        case ErrorType.NOT_FOUND:
            status_code = status.HTTP_404_NOT_FOUND
        case ErrorType.UNAUTHORIZED:
            status_code = status.HTTP_401_UNAUTHORIZED
        case ErrorType.FORBIDDEN:
            status_code = status.HTTP_403_FORBIDDEN
    error_data: ErrorData = ErrorData(title=err.title, detail=err.detail)
    return ErrorResponse(errors=[error_data], status=status_code).to_orjson()


async def unknown_exception_handler(request: Request, err: Exception) -> ORJSONResponse:  # noqa: ARG001
    logger.error("Handle error", exc_info=err, extra={"error": err})
    logger.exception("Unknown error occurred", exc_info=err, extra={"error": err})
    error_data: ErrorData = ErrorData(
        title="Unknown error occurred", detail="Unknown internal service error has occurred"
    )
    return ErrorResponse(
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        errors=[error_data],
    ).to_orjson()
