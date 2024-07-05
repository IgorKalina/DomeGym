from src.gym_management.domain.common import errors


class SubscriptionErrors:
    @staticmethod
    def cannot_have_more_rooms_than_subscription_allows() -> errors.Error:
        return errors.ValidationError(
            title="Number of allowed gyms has exceeded",
            description="A subscription cannot have more gyms than the subscription allows",
        )
