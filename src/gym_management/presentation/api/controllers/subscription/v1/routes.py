import typing
from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status
from fastapi.routing import APIRouter

from src.gym_management.application.admin.exceptions import AdminAlreadyExistsError
from src.gym_management.application.subscription.commands.create_subscription import CreateSubscription
from src.gym_management.application.subscription.queries.list_subscriptions import ListSubscriptions
from src.gym_management.infrastructure.common.injection.main import DiContainer
from src.gym_management.presentation.api.controllers.common.responses.dto import ErrorResponse, OkResponse
from src.gym_management.presentation.api.controllers.subscription.v1.requests.create_subscription_request import (
    CreateSubscriptionRequest,
)
from src.gym_management.presentation.api.controllers.subscription.v1.responses.subscription_response import (
    SubscriptionResponse,
)
from src.shared_kernel.application.command import CommandInvoker
from src.shared_kernel.application.query.interfaces.query_invoker import QueryInvoker

if typing.TYPE_CHECKING:
    from src.gym_management.domain.subscription.aggregate_root import Subscription


router = APIRouter(
    prefix="/v1/subscriptions",
    tags=["Subscriptions"],
)


@router.get(
    "",
    responses={
        status.HTTP_200_OK: {"model": OkResponse[SubscriptionResponse]},
    },
    response_model=OkResponse[SubscriptionResponse],
)
@inject
async def list_subscriptions(
    query_invoker: QueryInvoker = Depends(Provide[DiContainer.query_invoker]),
) -> OkResponse[SubscriptionResponse]:
    query = ListSubscriptions()
    result: List[Subscription] = await query_invoker.invoke(query)
    subscriptions_response = [
        SubscriptionResponse(
            id=subscription.id,
            type=subscription.type,
            created_at=subscription.created_at,
            admin_id=subscription.admin_id,
        )
        for subscription in result
    ]
    return OkResponse(status=status.HTTP_200_OK, data=subscriptions_response).to_orjson()


@router.post(
    "",
    responses={
        status.HTTP_201_CREATED: {"model": OkResponse[SubscriptionResponse]},
        status.HTTP_409_CONFLICT: {"model": ErrorResponse[AdminAlreadyExistsError]},
    },
    response_model=OkResponse[SubscriptionResponse],
)
@inject
async def create_subscription(
    request: CreateSubscriptionRequest,
    command_invoker: CommandInvoker = Depends(Provide[DiContainer.command_invoker]),
) -> OkResponse[SubscriptionResponse]:
    command = CreateSubscription(subscription_type=request.subscription_type, admin_id=request.admin_id)
    result: Subscription = await command_invoker.invoke(command)
    subscription_response = SubscriptionResponse(
        id=result.id,
        type=result.type,
        created_at=result.created_at,
        admin_id=result.admin_id,
    )
    return OkResponse(status=status.HTTP_201_CREATED, data=[subscription_response]).to_orjson()
