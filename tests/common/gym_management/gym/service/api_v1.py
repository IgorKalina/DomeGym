import uuid
from http import HTTPStatus
from typing import Tuple, TypeAlias

import httpx
from fastapi.testclient import TestClient

from src.gym_management.presentation.api.controllers.common.responses.dto import ErrorResponse, OkResponse
from src.gym_management.presentation.api.controllers.gyms.v1.requests.create_gym_request import CreateGymRequest
from src.gym_management.presentation.api.controllers.gyms.v1.responses.gym_response import GymResponse

ResponseData: TypeAlias = OkResponse[GymResponse] | ErrorResponse


class GymV1ApiService:
    def __init__(self, api_client: TestClient) -> None:
        self.__api_client = api_client

        self.__version = "v1"

    def create(self, request: CreateGymRequest, subscription_id: uuid.UUID) -> Tuple[httpx.Response, ResponseData]:
        response = self.__api_client.post(self.__get_url(subscription_id), json=request.model_dump())
        if response.status_code != HTTPStatus.CREATED:
            return response, ErrorResponse(status=response.status_code, **response.json())
        return response, OkResponse[GymResponse](status=response.status_code, **response.json())

    def __get_url(self, subscription_id: uuid.UUID) -> str:
        return f"{self.__version}/subscriptions/{str(subscription_id)}/gyms"
