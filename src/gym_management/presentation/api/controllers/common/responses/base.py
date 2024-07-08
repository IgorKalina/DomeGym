from typing import Optional

from fastapi import status

from src.common.error_or import ErrorOr
from src.gym_management.presentation.api.controllers.common.responses.adapters import (
    ErrorOrResponseAdapter as _ErrorOrResponseAdapter,
)
from src.gym_management.presentation.api.controllers.common.responses.adapters.error_or_adapter import ResponseData


def create_response(
    result: ErrorOr, ok_status_code: int = status.HTTP_200_OK, response_data_model: Optional[ResponseData] = None
):
    return _ErrorOrResponseAdapter(
        result=result,
        ok_status_code=ok_status_code,
        response_data_model=response_data_model,
    ).create_response()
