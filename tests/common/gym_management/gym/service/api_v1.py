import uuid
from http import HTTPStatus
from typing import Tuple

import httpx
from fastapi.testclient import TestClient

from src.gym_management.presentation.api.controllers.common.responses.dto import ErrorResponse, OkResponse, Response
from src.gym_management.presentation.api.controllers.gyms.v1.requests.create_gym_request import CreateGymRequest


class GymV1ApiService:
    def __init__(self, api_client: TestClient) -> None:
        self._api_client = api_client

        self._version = "v1"

    def create(self, request: CreateGymRequest, subscription_id: uuid.UUID) -> Tuple[httpx.Response, Response]:
        response = self._api_client.post(self._get_url(subscription_id), json=request.model_dump())
        if response.status_code != HTTPStatus.CREATED:
            return response, ErrorResponse(status=response.status_code, **response.json())
        return response, OkResponse(status=response.status_code, **response.json())

    def _get_url(self, subscription_id: uuid.UUID) -> str:
        return f"{self._version}/subscriptions/{str(subscription_id)}/gyms"
