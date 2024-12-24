from http import HTTPStatus
from typing import Tuple

import httpx
from fastapi.testclient import TestClient

from src.gym_management.presentation.api.controllers.common.responses.dto import ErrorResponse, OkResponse, Response
from src.gym_management.presentation.api.controllers.subscriptions.v1.requests.create_subscription_request import (
    CreateSubscriptionRequest,
)
from src.gym_management.presentation.api.controllers.subscriptions.v1.responses.subscription_response import (
    SubscriptionResponse,
)


class SubscriptionV1ApiService:
    def __init__(self, api_client: TestClient) -> None:
        self._api_client = api_client

        self._version = "v1"
        self._url = f"{self._version}/subscriptions"

    def create(self, request: CreateSubscriptionRequest) -> Tuple[httpx.Response, Response]:
        response = self._api_client.post(self._url, json=request.model_dump())
        if response.status_code != HTTPStatus.CREATED:
            return response, ErrorResponse(**response.json())
        return response, OkResponse[SubscriptionResponse](**response.json())

    def list(self) -> Tuple[httpx.Response, Response]:
        response = self._api_client.get(self._url)
        if response.status_code != HTTPStatus.OK:
            return response, ErrorResponse(**response.json())
        return response, OkResponse[SubscriptionResponse](**response.json())
