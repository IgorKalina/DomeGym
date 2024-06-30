from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status
from fastapi.routing import APIRouter

from src.gym_management.application.subscriptions.commands.create_subscription import (
    CreateSubscription,
    CreateSubscriptionHandler,
)
from src.gym_management.application.subscriptions.queries.list_subscriptions import (
    ListSubscriptions,
    ListSubscriptionsHandler,
)
from src.gym_management.presentation.api.controllers.common.responses.base import OkResponse
from src.gym_management.presentation.api.controllers.subscriptions.v1.requests.create_subscription_request import (
    CreateSubscriptionRequest,
)
from src.gym_management.presentation.api.controllers.subscriptions.v1.responses.subscription_response import (
    SubscriptionResponse,
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
@inject
async def list_subscriptions(
    query_handler: ListSubscriptionsHandler = Depends(
        Provide[DependencyContainer.app_container.list_subscriptions_handler]
    ),
) -> OkResponse:
    query = ListSubscriptions()
    result = await query_handler.handle(query)
    return OkResponse(
        status=status.HTTP_200_OK,
        result=[
            SubscriptionResponse(
                id=subscription.id,
                type=subscription.type,
                admin_id=subscription.admin_id,
                created_at=subscription.created_at,
            )
            for subscription in result
        ],
    )
