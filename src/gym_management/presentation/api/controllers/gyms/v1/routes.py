import typing
import uuid

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status
from fastapi.routing import APIRouter

from src.gym_management.application.gyms.commands.create_gym import CreateGym
from src.gym_management.infrastructure.subscriptions.injection.main import SubscriptionsContainer
from src.gym_management.presentation.api.controllers.common.responses.base import create_response
from src.gym_management.presentation.api.controllers.common.responses.dto import OkResponse
from src.gym_management.presentation.api.controllers.gyms.v1.requests.create_gym_request import CreateGymRequest
from src.shared_kernel.application.command import CommandInvoker

if typing.TYPE_CHECKING:
    from src.shared_kernel.application.error_or import ErrorOr


router = APIRouter(
    prefix="/v1/subscriptions/{subscription_id}/gyms",
    tags=["Gyms"],
)


@router.post("")
@inject
async def create_gym(
    request: CreateGymRequest,
    subscription_id: uuid.UUID,
    command_invoker: CommandInvoker = Depends(Provide[SubscriptionsContainer.commands_invoker]),
) -> OkResponse:
    command = CreateGym(name=request.name, subscription_id=subscription_id)
    result: ErrorOr = await command_invoker.invoke(command)
    return create_response(result=result, ok_status_code=status.HTTP_201_CREATED)
