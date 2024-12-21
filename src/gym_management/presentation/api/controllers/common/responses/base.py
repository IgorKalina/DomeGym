from typing import Any, Optional

from fastapi import status

from src.gym_management.presentation.api.controllers.common.responses.adapters import (
    ErrorOrResponseAdapter as _ErrorOrResponseAdapter,
)
from src.gym_management.presentation.api.controllers.common.responses.adapters.error_or_adapter import ResponseData
from src.shared_kernel.application.error_or import ErrorOr


def create_response(  # noqa: ANN201
    result: ErrorOr | Any, ok_status_code: int = status.HTTP_200_OK, response_data_model: Optional[ResponseData] = None
):
    return _ErrorOrResponseAdapter(
        result=result,
        ok_status_code=ok_status_code,
        response_data_model=response_data_model,
    ).create_response()
