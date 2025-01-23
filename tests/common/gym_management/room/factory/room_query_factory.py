import uuid

from src.gym_management.application.room.queries.list_rooms import ListRooms
from tests.common.gym_management.common import constants


class RoomQueryFactory:
    @staticmethod
    def create_list_rooms_query(
        gym_id: uuid.UUID = constants.gym.GYM_ID,
        subscription_id: uuid.UUID = constants.subscription.SUBSCRIPTION_ID,
    ) -> ListRooms:
        return ListRooms(gym_id=gym_id, subscription_id=subscription_id)
