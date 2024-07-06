from src.common.error_or import Error


class GymErrors:
    @staticmethod
    def cannot_have_more_rooms_than_subscription_allows() -> Error:
        return Error.validation(description="A gym cannot have more rooms than the subscription allows")

    @staticmethod
    def cannot_remove_not_existing_room() -> Error:
        return Error.not_found(description="Given room does not exists in the gym")
