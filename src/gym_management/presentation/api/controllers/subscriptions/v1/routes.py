import typing
from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status
from fastapi.routing import APIRouter

from src.common.mediator.interfaces import ICommandMediator, IQueryMediator
from src.gym_management.application.subscriptions.commands.create_subscription import CreateSubscription
from src.gym_management.application.subscriptions.errors import AdminAlreadyExists
from src.gym_management.application.subscriptions.queries.list_subscriptions import ListSubscriptions
from src.gym_management.presentation.api.controllers.common.responses.base import create_response
from src.gym_management.presentation.api.controllers.common.responses.dto import ErrorResponse, OkResponse
from src.gym_management.presentation.api.controllers.subscriptions.v1.requests.create_subscription_request import (
    CreateSubscriptionRequest,
)
from src.gym_management.presentation.api.controllers.subscriptions.v1.responses.subscription_response import (
    SubscriptionResponse,
)
from src.gym_management.presentation.api.dependency_injection import DependencyContainer

if typing.TYPE_CHECKING:
    from src.common.error_or import ErrorOr
    from src.gym_management.domain.subscription.aggregate_root import Subscription


router = APIRouter(
    prefix="/v1/subscriptions",
    tags=["Subscriptions"],
)


@router.post(
    "",
    responses={
        status.HTTP_409_CONFLICT: {"model": ErrorResponse[AdminAlreadyExists]},
    },
)
@inject
async def create_subscription(
    request: CreateSubscriptionRequest,
    mediator: ICommandMediator = Depends(Provide[DependencyContainer.get_mediator()]),
) -> OkResponse:
    command = CreateSubscription(subscription_type=request.subscription_type, admin_id=request.admin_id)
    result: ErrorOr = await mediator.send(command)
    return create_response(result=result, ok_status_code=status.HTTP_201_CREATED)


@router.get(
    "",
    responses={
        status.HTTP_200_OK: {"model": OkResponse[SubscriptionResponse]},
    },
    response_model=OkResponse[SubscriptionResponse],
)
@inject
async def list_subscriptions(
    mediator: IQueryMediator = Depends(Provide[DependencyContainer.get_mediator()]),
) -> SubscriptionResponse:
    query = ListSubscriptions()
    result: List[Subscription] = await mediator.query(query)
    return create_response(
        result=result,
        ok_status_code=status.HTTP_200_OK,
        response_data_model=SubscriptionResponse,  # type: ignore
    )
