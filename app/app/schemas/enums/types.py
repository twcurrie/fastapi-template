import logging
from enum import Enum, IntEnum


class CaseInsensitiveEnum(Enum):
    @classmethod
    def _missing_(cls, value):
        """Make lookup case-insensitive"""
        for member in cls:
            if member.name.casefold() == value.casefold():
                return member
        raise ValueError("%r is not a valid %s" % (value, cls.__name__))


class CaseInsensitiveEnumWithDefault(Enum):
    @classmethod
    def _missing_(cls, value):
        """Default to `cls.default` if not found."""
        for member in cls:
            if member.name.casefold() == value.casefold():
                return member
        logging.info(f"Defaulting value of {value} to {cls.default}")
        return cls.default
