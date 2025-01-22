import typing
import uuid
from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status
from fastapi.routing import APIRouter

from src.gym_management.application.room.commands.create_room import CreateRoom
from src.gym_management.application.room.queries.list_rooms import ListRooms
from src.gym_management.infrastructure.common.injection.main import DiContainer
from src.gym_management.presentation.api.controllers.common.responses.dto import OkResponse
from src.gym_management.presentation.api.controllers.common.responses.orjson import ORJSONResponse
from src.gym_management.presentation.api.controllers.room.v1.requests.create_gym_request import CreateRoomRequest
from src.gym_management.presentation.api.controllers.room.v1.responses.room_response import RoomResponse
from src.shared_kernel.application.command import CommandInvoker
from src.shared_kernel.application.query.interfaces.query_invoker import QueryInvoker

if typing.TYPE_CHECKING:
    from src.gym_management.application.common.dto.repository.room import RoomDB


router = APIRouter(
    prefix="/v1/subscriptions/{subscription_id}/gyms/{gym_id}/rooms",
    tags=["Rooms"],
)


@router.post(
    "",
    response_model=OkResponse[RoomResponse],
)
@inject
async def create_room(
    request: CreateRoomRequest,
    subscription_id: uuid.UUID,
    gym_id: uuid.UUID,
    command_invoker: CommandInvoker = Depends(Provide[DiContainer.command_invoker]),
) -> ORJSONResponse:
    command = CreateRoom(name=request.name, gym_id=gym_id, subscription_id=subscription_id)
    room: RoomDB = await command_invoker.invoke(command)
    room_response: RoomResponse = RoomResponse(
        id=room.id, name=room.name, gym_id=room.gym_id, subscription_id=room.subscription_id, created_at=room.created_at
    )
    return OkResponse(status=status.HTTP_201_CREATED, data=[room_response]).to_orjson()


@router.get(
    "",
    response_model=OkResponse[RoomResponse],
)
@inject
async def list_rooms(
    gym_id: uuid.UUID,
    subscription_id: uuid.UUID,
    query_invoker: QueryInvoker = Depends(Provide[DiContainer.query_invoker]),
) -> ORJSONResponse:
    query = ListRooms(gym_id=gym_id, subscription_id=subscription_id)
    rooms: List[RoomDB] = await query_invoker.invoke(query)
    response: List[RoomResponse] = [
        RoomResponse(
            id=room.id,
            name=room.name,
            gym_id=room.gym_id,
            subscription_id=room.subscription_id,
            created_at=room.created_at,
        )
        for room in rooms
    ]
    return OkResponse(status=status.HTTP_200_OK, data=response).to_orjson()
