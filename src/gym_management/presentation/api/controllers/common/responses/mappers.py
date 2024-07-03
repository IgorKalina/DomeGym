from fastapi import status

from src.gym_management.domain.common.errors import ErrorType


def map_error_type_to_http_status(error_type: ErrorType) -> int:
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
