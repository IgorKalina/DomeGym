from src.common.error_or import Error


class SubscriptionErrors:
    @staticmethod
    def cannot_have_more_rooms_than_subscription_allows() -> Error:
        return Error.validation(
            description="A subscription cannot have more gyms than the subscription allows",
        )
