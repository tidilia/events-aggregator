from enum import Enum

class EventStatus(str, Enum):
    PUBLISHED = "published"
    NEW = "new"
    REGISTRATION_CLOSED = "registration_closed"
    FINISHED = "finished"