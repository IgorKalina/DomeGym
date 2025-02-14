import typing
import uuid

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status
from fastapi.routing import APIRouter

from src.gym_management.application.gym.commands.create_gym import CreateGym
from src.gym_management.application.gym.commands.remove_gym import RemoveGym
from src.gym_management.application.gym.queries.get_gym import GetGym
from src.gym_management.application.gym.queries.list_gyms import ListGyms
from src.gym_management.infrastructure.common.injection.main import DiContainer
from src.gym_management.presentation.api.controllers.common.responses.dto import OkResponse
from src.gym_management.presentation.api.controllers.common.responses.orjson import ORJSONResponse
from src.gym_management.presentation.api.controllers.gym.v1.requests.create_gym_request import CreateGymRequest
from src.gym_management.presentation.api.controllers.gym.v1.responses.gym_response import GymResponse
from src.shared_kernel.application.command import CommandBus
from src.shared_kernel.application.query.interfaces.query_bus import QueryBus

if typing.TYPE_CHECKING:
    from src.gym_management.application.common.dto.repository import GymDB

router = APIRouter(
    prefix="/v1/subscriptions/{subscription_id}/gyms",
    tags=["Gyms"],
)


@router.post(
    "",
    response_model=OkResponse[GymResponse],
)
@inject
async def create_gym(
    request: CreateGymRequest,
    subscription_id: uuid.UUID,
    command_bus: CommandBus = Depends(Provide[DiContainer.command_bus]),
) -> ORJSONResponse:
    command = CreateGym(name=request.name, subscription_id=subscription_id)
    gym: GymDB = await command_bus.invoke(command)
    gym_response: GymResponse = GymResponse(
        id=gym.id, name=gym.name, subscription_id=gym.subscription_id, created_at=gym.created_at
    )
    return OkResponse(status=status.HTTP_201_CREATED, data=[gym_response]).to_orjson()


@router.get(
    "/{gym_id}",
    response_model=OkResponse[GymResponse],
)
@inject
async def get_gym(
    gym_id: uuid.UUID,
    subscription_id: uuid.UUID,
    query_bus: QueryBus = Depends(Provide[DiContainer.query_bus]),
) -> ORJSONResponse:
    query = GetGym(gym_id=gym_id, subscription_id=subscription_id)
    gym: GymDB = await query_bus.invoke(query)
    gym_response: GymResponse = GymResponse(
        id=gym.id, name=gym.name, subscription_id=gym.subscription_id, created_at=gym.created_at
    )
    return OkResponse(status=status.HTTP_200_OK, data=[gym_response]).to_orjson()


@router.get(
    "",
    response_model=OkResponse[GymResponse],
)
@inject
async def list_gyms(
    subscription_id: uuid.UUID,
    query_bus: QueryBus = Depends(Provide[DiContainer.query_bus]),
) -> ORJSONResponse:
    query = ListGyms(subscription_id=subscription_id)
    gyms: typing.List[GymDB] = await query_bus.invoke(query)
    gym_response: typing.List[GymResponse] = [
        GymResponse(id=gym.id, name=gym.name, subscription_id=gym.subscription_id, created_at=gym.created_at)
        for gym in gyms
    ]
    return OkResponse(status=status.HTTP_200_OK, data=gym_response).to_orjson()


@router.delete(
    "/{gym_id}",
    response_model=OkResponse[GymResponse],
    responses={
        status.HTTP_204_NO_CONTENT: {},
    },
)
@inject
async def remove_gym(
    gym_id: uuid.UUID,
    subscription_id: uuid.UUID,
    command_bus: CommandBus = Depends(Provide[DiContainer.command_bus]),
) -> ORJSONResponse:
    command = RemoveGym(gym_id=gym_id, subscription_id=subscription_id)
    await command_bus.invoke(command)
    return OkResponse(status=status.HTTP_204_NO_CONTENT).to_orjson()
