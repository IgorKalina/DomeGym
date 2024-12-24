import typing
from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status
from fastapi.routing import APIRouter

from src.gym_management.application.subscriptions.commands.create_subscription import CreateSubscription
from src.gym_management.application.subscriptions.errors import AdminAlreadyExists
from src.gym_management.application.subscriptions.queries.list_subscriptions import ListSubscriptions
from src.gym_management.infrastructure.common.injection.main import DiContainer
from src.gym_management.presentation.api.controllers.common.responses.base import create_response
from src.gym_management.presentation.api.controllers.common.responses.dto import ErrorResponse, OkResponse
from src.gym_management.presentation.api.controllers.subscriptions.v1.requests.create_subscription_request import (
    CreateSubscriptionRequest,
)
from src.gym_management.presentation.api.controllers.subscriptions.v1.responses.subscription_response import (
    SubscriptionResponse,
)
from src.shared_kernel.application.command import CommandInvoker
from src.shared_kernel.application.query.interfaces.query_invoker import QueryInvoker

if typing.TYPE_CHECKING:
    from src.gym_management.domain.subscription.aggregate_root import Subscription
    from src.shared_kernel.application.error_or import ErrorOr


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
) -> List[SubscriptionResponse]:
    query = ListSubscriptions()
    result: List[Subscription] = await query_invoker.invoke(query)
    return create_response(
        result=result,
        ok_status_code=status.HTTP_200_OK,
        data=[
            SubscriptionResponse(
                id=subscription.id,
                type=subscription.type,
                created_at=subscription.created_at,
                admin_id=subscription.admin_id,
            )
            for subscription in result
        ],
    )


@router.post(
    "",
    responses={
        status.HTTP_409_CONFLICT: {"model": ErrorResponse[AdminAlreadyExists]},
    },
    response_model=OkResponse[SubscriptionResponse],
)
@inject
async def create_subscription(
    request: CreateSubscriptionRequest,
    command_invoker: CommandInvoker = Depends(Provide[DiContainer.command_invoker]),
) -> OkResponse:
    command = CreateSubscription(subscription_type=request.subscription_type, admin_id=request.admin_id)
    result: ErrorOr[Subscription] = await command_invoker.invoke(command)
    return create_response(
        result=result,
        ok_status_code=status.HTTP_201_CREATED,
        data=[
            SubscriptionResponse(
                id=result.value.id,
                type=result.value.type,
                created_at=result.value.created_at,
                admin_id=result.value.admin_id,
            )
        ]
        if result.is_ok()
        else [],
    )
