from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status
from fastapi.routing import APIRouter

from src.gym_management.application.subscriptions.commands.create_subscription import (
    CreateSubscription,
    CreateSubscriptionHandler,
)
from src.gym_management.presentation.api.controllers.common.responses.base import OkResponse
from src.gym_management.presentation.api.controllers.subscriptions.v1.requests.create_subscription_request import (
    CreateSubscriptionRequest,
)
from src.gym_management.presentation.api.dependency_injection import DependencyContainer

router = APIRouter(
    prefix="/v1/subscriptions",
    tags=["subscriptions"],
)


@router.post("/")
@inject
async def create_subscription(
    request: CreateSubscriptionRequest,
    command_handler: CreateSubscriptionHandler = Depends(
        Provide[DependencyContainer.app_container.create_subscription_handler]
    ),
) -> OkResponse:
    command = CreateSubscription(subscription_type=request.subscription_type, admin_id=request.admin_id)
    result = await command_handler.handle(command)
    return OkResponse(status=status.HTTP_200_OK, result=result.value)


@router.get(
    "",
)
async def list_subscriptions() -> OkResponse:
    """
    List gyms
    """
    return OkResponse(status=status.HTTP_200_OK)
