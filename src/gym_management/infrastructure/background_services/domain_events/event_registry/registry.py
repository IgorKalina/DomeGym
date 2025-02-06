from typing import Type

from src.gym_management.domain.admin.events.subscription_set_event import SubscriptionSetEvent
from src.gym_management.domain.admin.events.subscription_unset_event import SubscriptionUnsetEvent
from src.gym_management.domain.gym.events.room_added_event import RoomAddedEvent
from src.gym_management.domain.gym.events.room_removed_event import RoomRemovedEvent
from src.gym_management.domain.subscription.events.gym_added_event import GymAddedEvent
from src.gym_management.domain.subscription.events.gym_removed_event import GymRemovedEvent
from src.gym_management.infrastructure.background_services.domain_events.event_registry.domain_event_type import (
    DomainEventType,
)
from src.shared_kernel.domain.common.event import DomainEvent


class DomainEventRegistry:
    def __init__(self) -> None:
        self.__type_to_class = {
            # subscription
            DomainEventType.SUBSCRIPTION_SET: SubscriptionSetEvent,
            DomainEventType.SUBSCRIPTION_UNSET: SubscriptionUnsetEvent,
            # gym
            DomainEventType.GYM_ADDED: GymAddedEvent,
            DomainEventType.GYM_REMOVED: GymRemovedEvent,
            # room
            DomainEventType.ROOM_ADDED: RoomAddedEvent,
            DomainEventType.ROOM_REMOVED: RoomRemovedEvent,
        }

        self.__class_to_type = {event_class: event_type for event_type, event_class in self.__type_to_class.items()}

    def get_event_type(self, event: DomainEvent) -> DomainEventType:
        event_type = self.__class_to_type.get(type(event))
        if event_type is None:
            raise ValueError(
                f"Domain event type does not exist for event class '{type(event).__name__}'. "
                f"Did you forget to add it to registry?"
            )
        return event_type

    def get_event_class(self, event_type: DomainEventType) -> Type[DomainEvent]:
        event_class = self.__type_to_class.get(event_type)
        if event_class is None:
            raise ValueError(
                f"Domain event class does not exist for event type '{str(event_type)}'. "
                f"Did you forget to add it to registry?"
            )
        return event_class
