from typing import Any, List

from fastapi import status

from src.gym_management.presentation.api.controllers.common.responses.adapters import (
    ErrorOrResponseAdapter as _ErrorOrResponseAdapter,
)
from src.gym_management.presentation.api.controllers.common.responses.dto import ResponseData
from src.shared_kernel.application.error_or import ErrorOr


def create_response(  # noqa: ANN201
    result: ErrorOr | Any, ok_status_code: int = status.HTTP_200_OK, data: List[ResponseData] | None = None
):
    data = data or []
    return _ErrorOrResponseAdapter(
        result=result,
        ok_status_code=ok_status_code,
        data=data,
    ).create_response()
