import json
from datetime import datetime, date

import sqlalchemy as sa  # type: ignore
from pydantic import parse_obj_as

from app.core.monitoring import contains_phi


def _map_to_type(value, type_):
    """
    General mapping of an arbitrary value to a specific type.

    This function is used by the `PHIType` to handle the conversion
    from the return value class to the `contains_phi` decorated class
    that occurs when a value is handled by the custom TypeDecorator.
    """
    if isinstance(value, type_):
        return value
    if issubclass(type_, date):
        if isinstance(value, str):
            value = parse_obj_as(date, value)
        return type_(year=value.year, month=value.month, day=value.day)
    elif issubclass(type_, datetime):
        if isinstance(value, str):
            value = parse_obj_as(date, value)
        return type_(
            year=value.year,
            month=value.month,
            day=value.day,
            hour=value.hour,
            minute=value.minute,
            second=value.minute,
            microsecond=value.microsecond,
            tzinfo=value.tzinfo,
        )
    elif issubclass(type_, dict):
        if isinstance(value, str):
            return type_(json.loads(value))
        else:
            raise ValueError(f"Cannot handle the mapping from {type(value)} to {type_}")
    else:
        return type_(value)


class PHIType(sa.TypeDecorator):
    """
    This is a generalized type that leverages the SQLAlchemy's TypeDecorator to
    provide additional formatting of data stored in columns that hides the sensitive
    information.

    Please reference SQLAlchemy's documentation for further details on TypeDecorators:
    https://github.com/zzzeek/sqlalchemy/blob/master/lib/sqlalchemy/sql/type_api.py#L858-L970
    """

    def __new__(cls, name, base_type, sqlalchemy_type, *args, **kwargs):
        """
        This constructs the class for the new SQLAlchemy type class, prior to
        any instantiations for the specified type that it handles and produces.
        """
        if cls is PHIType:
            type_ = type(name, (sa.TypeDecorator,), {})
            type_.impl = sqlalchemy_type
            type_.cache_ok = False

            type_.process_bind_param = cls._process_bind_param(
                implementation=contains_phi(type(name, (base_type,), {}))
            )
            type_.process_literal_param = cls._process_literal_param(
                implementation=contains_phi(type(name, (base_type,), {}))
            )
            type_.process_result_value = cls._process_result_value(
                implementation=contains_phi(type(name, (base_type,), {}))
            )
            return type_
        # To support the construction of other objects on the MRO, we must call
        # this method to ensure other classes' __new__ methods can be called.
        return object.__new__(cls)

    @staticmethod
    def _process_bind_param(implementation):
        def process_bind_param(self, value, dialect):
            if value is not None:
                value = _map_to_type(value, implementation)
                return value
            return value

        return process_bind_param

    @staticmethod
    def _process_literal_param(implementation):
        def process_literal_param(self, value, dialect):
            if value is not None and not isinstance(value, implementation):
                value = _map_to_type(value, implementation)
                return value
            return value

        return process_literal_param

    @staticmethod
    def _process_result_value(implementation):
        def process_result_value(self, value, dialect):
            if value is not None:
                value = _map_to_type(value, implementation)
                return value
            return value

        return process_result_value


Date = PHIType(name="Date", base_type=date, sqlalchemy_type=sa.Date)
DateTime = PHIType(name="DateTime", base_type=datetime, sqlalchemy_type=sa.DateTime)
Integer = PHIType(name="Integer", base_type=int, sqlalchemy_type=sa.Integer)
JSON = PHIType(name="JSON", base_type=dict, sqlalchemy_type=sa.JSON)
String = PHIType(name="String", base_type=str, sqlalchemy_type=sa.String)
