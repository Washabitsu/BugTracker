from enum import Enum

class Severity(Enum):
    CRITICAL = "CRITICAL"
    MAJOR = "MAJOR"
    MINOR = "MINOR"
    TRIVIAL = "TRIVIAL"
    ENHANCEMENT = "ENHANCEMENT"

class Severity(str,Enum):
    CRITICAL = Severity.CRITICAL.name
    MAJOR = Severity.MAJOR.name
    MINOR = Severity.MINOR.name
    TRIVIAL = Severity.TRIVIAL.name
    ENHANCEMENT = Severity.ENHANCEMENT.name
    