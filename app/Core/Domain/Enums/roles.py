from enum import Enum

class Roles(Enum):
    DEVELOPER = "DEVELOPER"
    TESTER = "TESTER"
    ADMINISTRATOR = "ADMINISTRATOR"

class Roles(str,Enum):
    DEVELOPER = Roles.DEVELOPER.name
    TESTER = Roles.TESTER.name
    ADMINISTRATOR = Roles.ADMINISTRATOR.name
    