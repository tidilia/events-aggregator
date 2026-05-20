from enum import Enum


class EventStatus(str, Enum):
    published = "published"
    new = "new"
    registration_closed = "registration_closed"
    finished = "finished"
