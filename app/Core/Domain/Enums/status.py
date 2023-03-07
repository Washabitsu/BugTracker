from enum import Enum

class Status(Enum):
    NEW = "NEW"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    FIXED = "FIXED"
    VERIFIED = "VERIFIED"
    CLOSED = "CLOSED"
    DEFERRED = "DEFERRED"
    DUPLICATE = "DUPLICATE"

class Status(str,Enum):
    NEW = Status.NEW.name
    ASSIGNED = Status.ASSIGNED.name
    IN_PROGRESS = Status.IN_PROGRESS.name
    FIXED = Status.FIXED.name
    VERIFIED =Status.VERIFIED.name
    CLOSED = Status.CLOSED.name
    DEFERRED = Status.DEFERRED.name
    DUPLICATE = Status.DUPLICATE.name