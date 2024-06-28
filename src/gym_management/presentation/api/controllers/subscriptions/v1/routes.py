from fastapi import status
from fastapi.routing import APIRouter

from src.gym_management.application.subscriptions.commands.create_subscription import (
    CreateSubscription,
    CreateSubscriptionHandler,
)
from src.gym_management.infrastructure.admins.persistence.repositories.memory_repository import AdminsMemoryRepository
from src.gym_management.presentation.api.controllers.common.responses.base import OkResponse
from src.gym_management.presentation.api.controllers.subscriptions.v1.requests.create_subscription_request import (
    CreateSubscriptionRequest,
)

router = APIRouter(
    prefix="/v1/subscriptions",
    tags=["subscriptions"],
)


@router.post(
    "/",
)
async def create_subscription(request: CreateSubscriptionRequest) -> OkResponse:
    command = CreateSubscription(subscription_type=request.subscription_type, admin_id=request.admin_id)
    result = await CreateSubscriptionHandler(admins_repository=AdminsMemoryRepository()).handle(command)
    return OkResponse(status=status.HTTP_200_OK, result=result.value)


@router.get(
    "",
)
async def list_subscriptions() -> OkResponse:
    """
    List gyms
    """
    return OkResponse(status=status.HTTP_200_OK)
