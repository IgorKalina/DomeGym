from enum import StrEnum


class DomainEventType(StrEnum):
    SUBSCRIPTION_SET = "subscription_set"
    SUBSCRIPTION_UNSET = "subscription_unset"
    GYM_REMOVED = "gym_removed"
    GYM_ADDED = "gym_added"
    ROOM_ADDED = "room_added"
    ROOM_REMOVED = "room_removed"
    SOME_EVENT = "some_event"
