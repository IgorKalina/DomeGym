import uuid
from http import HTTPStatus
from typing import Tuple, TypeAlias

import httpx
from fastapi import HTTPException
from fastapi.testclient import TestClient

from src.gym_management.presentation.api.controllers.common.responses.dto import ErrorResponse, OkResponse
from src.gym_management.presentation.api.controllers.subscription.v1.requests.create_subscription_request import (
    CreateSubscriptionRequest,
)
from src.gym_management.presentation.api.controllers.subscription.v1.responses.subscription_response import (
    SubscriptionResponse,
)

ResponseData: TypeAlias = OkResponse[SubscriptionResponse] | ErrorResponse


class SubscriptionV1ApiService:
    def __init__(self, api_client: TestClient) -> None:
        self.__api_client = api_client

        self.__version = "v1"
        self.__url = f"{self.__version}/subscriptions"

    def create(self, request: CreateSubscriptionRequest) -> Tuple[httpx.Response, ResponseData]:
        response = self.__api_client.post(self.__url, json=request.model_dump())
        if response.status_code != HTTPStatus.CREATED:
            return response, ErrorResponse(status=response.status_code, **response.json())
        return response, OkResponse[SubscriptionResponse](status=response.status_code, **response.json())

    def list(self) -> Tuple[httpx.Response, ResponseData]:
        response = self.__api_client.get(self.__url)
        if response.status_code != HTTPStatus.OK:
            return response, ErrorResponse(status=response.status_code, **response.json())
        return response, OkResponse[SubscriptionResponse](status=response.status_code, **response.json())

    def get_subscription_by_admin_id(self, admin_id: uuid.UUID) -> SubscriptionResponse:
        response, subscriptions = self.list()
        response.raise_for_status()
        for subscription in subscriptions.data:
            if subscription.admin_id == admin_id:
                return subscription
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Subscription for the given admin id not found")
