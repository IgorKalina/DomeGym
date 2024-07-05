import uuid

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status
from fastapi.routing import APIRouter

from src.gym_management.application.gyms.commands.create_gym import CreateGym, CreateGymHandler
from src.gym_management.presentation.api.controllers.common.responses.base import ResultResponseAdapter
from src.gym_management.presentation.api.controllers.common.responses.orjson import ORJSONResponse
from src.gym_management.presentation.api.controllers.gyms.v1.requests.create_gym_request import CreateGymRequest
from src.gym_management.presentation.api.dependency_injection import DependencyContainer

router = APIRouter(
    prefix="/v1/subscriptions/{subscription_id}/gyms",
    tags=["gyms"],
)


@router.post("")
@inject
async def create_gym(
    request: CreateGymRequest,
    subscription_id: uuid.UUID,
    command_handler: CreateGymHandler = Depends(Provide[DependencyContainer.app_container.create_gym_handler]),
) -> ORJSONResponse:
    command = CreateGym(name=request.name, subscription_id=subscription_id)
    result = await command_handler.handle(command)
    return ResultResponseAdapter(result=result, ok_status_code=status.HTTP_200_OK).create_response()
