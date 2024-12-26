import typing
import uuid

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status
from fastapi.routing import APIRouter

from src.gym_management.application.gyms.commands.create_gym import CreateGym
from src.gym_management.infrastructure.common.injection.main import DiContainer
from src.gym_management.presentation.api.controllers.common.responses.dto import OkResponse
from src.gym_management.presentation.api.controllers.common.responses.orjson import ORJSONResponse
from src.gym_management.presentation.api.controllers.gyms.v1.requests.create_gym_request import CreateGymRequest
from src.gym_management.presentation.api.controllers.gyms.v1.responses.gym_response import GymResponse
from src.shared_kernel.application.command import CommandInvoker

if typing.TYPE_CHECKING:
    from src.gym_management.domain.gym.aggregate_root import Gym


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
    command_invoker: CommandInvoker = Depends(Provide[DiContainer.command_invoker]),
) -> ORJSONResponse:
    command = CreateGym(name=request.name, subscription_id=subscription_id)
    gym: Gym = await command_invoker.invoke(command)
    gym_response: GymResponse = GymResponse(
        id=gym.id, name=gym.name, subscription_id=gym.subscription_id, created_at=gym.created_at
    )
    return OkResponse(status=status.HTTP_201_CREATED, data=[gym_response]).to_orjson()
