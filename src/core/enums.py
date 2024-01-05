
from enum import Enum

class ExtendedEnum(Enum):

    @classmethod
    @property
    def keys(cls):
        return cls._member_names_

    @classmethod
    @property
    def values(cls):
        return [item.value for item in list(cls)]

# supported engines
class DBEngine(ExtendedEnum):
    SQLITE = 'sqlite+aiosqlite'
    POSTGRES = 'postgresql+asyncpg'
