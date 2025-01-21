import uuid
from http import HTTPStatus
from typing import Tuple, TypeAlias

import httpx
from httpx import AsyncClient

from src.gym_management.presentation.api.controllers.common.responses.dto import ErrorResponse, OkResponse
from src.gym_management.presentation.api.controllers.room.v1.requests.create_gym_request import CreateRoomRequest
from src.gym_management.presentation.api.controllers.room.v1.responses.room_response import RoomResponse

ResponseData: TypeAlias = OkResponse[RoomResponse] | ErrorResponse


class RoomV1ApiService:
    def __init__(self, api_client: AsyncClient) -> None:
        self.__api_client = api_client

        self.__version = "v1"

    async def create(
        self,
        request: CreateRoomRequest,
        subscription_id: uuid.UUID,
        gym_id: uuid.UUID,
    ) -> Tuple[httpx.Response, ResponseData]:
        response = await self.__api_client.post(
            url=self.__get_url(subscription_id=subscription_id, gym_id=gym_id), json=request.model_dump()
        )
        if response.status_code != HTTPStatus.CREATED:
            return response, ErrorResponse(status=response.status_code, **response.json())
        return response, OkResponse[RoomResponse](status=response.status_code, **response.json())

    async def list(self, gym_id: uuid.UUID, subscription_id: uuid.UUID) -> Tuple[httpx.Response, ResponseData]:
        response = await self.__api_client.get(url=self.__get_url(subscription_id=subscription_id, gym_id=gym_id))
        if response.status_code != HTTPStatus.OK:
            return response, ErrorResponse(status=response.status_code, **response.json())
        return response, OkResponse[RoomResponse](status=response.status_code, **response.json())

    def __get_url(self, subscription_id: uuid.UUID, gym_id: uuid.UUID) -> str:
        return f"{self.__version}/subscriptions/{subscription_id}/gyms/{gym_id}/rooms"
