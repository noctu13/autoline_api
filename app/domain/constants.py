from enum import Enum

class RoleID(Enum):
    ADMIN = 1
    DISPATCHER = 2
    DRIVER = 3
    PASSENGER = 4
    
    @classmethod
    def values_set(cls):
        return {member.value for member in cls}