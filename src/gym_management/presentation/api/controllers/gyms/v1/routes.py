from fastapi import status
from fastapi.routing import APIRouter

from src.gym_management.presentation.api.controllers.common.responses.base import OkResponse

router = APIRouter(
    prefix="/v1/subscriptions/{subscription_id}/gyms",
    tags=["gyms"],
)


@router.get(
    "",
)
async def list_gyms() -> OkResponse:
    """
    List gyms
    """
    return OkResponse(status=status.HTTP_200_OK)
