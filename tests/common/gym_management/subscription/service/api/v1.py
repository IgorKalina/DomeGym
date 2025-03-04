import uuid
from http import HTTPStatus
from typing import Tuple, TypeAlias

import httpx
from httpx import AsyncClient

from src.gym_management.presentation.api.controllers.common.responses.dto import ErrorResponse, OkResponse
from src.gym_management.presentation.api.controllers.subscription.v1.requests.create_subscription_request import (
    CreateSubscriptionRequest,
)
from src.gym_management.presentation.api.controllers.subscription.v1.responses.subscription_response import (
    SubscriptionResponse,
)

ResponseData: TypeAlias = OkResponse[SubscriptionResponse] | ErrorResponse


class SubscriptionV1ApiService:
    def __init__(self, api_client: AsyncClient) -> None:
        self.__api_client = api_client

        self.__version = "v1"
        self.__url = f"{self.__version}/subscriptions"

    async def create(self, request: CreateSubscriptionRequest) -> Tuple[httpx.Response, ResponseData]:
        response = await self.__api_client.post(self.__url, json=request.model_dump())
        if response.status_code != HTTPStatus.CREATED:
            return response, ErrorResponse(status=response.status_code, **response.json())
        return response, OkResponse[SubscriptionResponse](status=response.status_code, **response.json())

    async def get(self, subscription_id: uuid.UUID) -> Tuple[httpx.Response, ResponseData]:
        response = await self.__api_client.get(f"{self.__url}/{subscription_id}")
        if response.status_code != HTTPStatus.OK:
            return response, ErrorResponse(status=response.status_code, **response.json())
        return response, OkResponse[SubscriptionResponse](status=response.status_code, **response.json())

    async def delete(self, subscription_id: uuid.UUID) -> Tuple[httpx.Response, ResponseData]:
        response = await self.__api_client.delete(f"{self.__url}/{subscription_id}")
        if response.status_code != HTTPStatus.OK:
            return response, ErrorResponse(status=response.status_code, **response.json())
        return response, OkResponse[SubscriptionResponse](status=response.status_code, **response.json())

    async def list(self) -> Tuple[httpx.Response, ResponseData]:
        response = await self.__api_client.get(self.__url)
        if response.status_code != HTTPStatus.OK:
            return response, ErrorResponse(status=response.status_code, **response.json())
        return response, OkResponse[SubscriptionResponse](status=response.status_code, **response.json())
