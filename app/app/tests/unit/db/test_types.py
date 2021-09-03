import pytest
from datetime import date, datetime
from app.db.types.phi_column import _map_to_type


@pytest.mark.parametrize(
    "value, mapped_type, expected",
    [
        ("2012-01-01", date, date(2012, 1, 1)),
        ("2011-01-01", datetime, datetime(2011, 1, 1)),
        ("1", int, 1),
        ("1", str, "1"),
        ("true", bool, True),
        ({"a": "b", "c": "d"}, dict, {"a": "b", "c": "d"}),
        ('{"a": "b", "c": "d"}', dict, {"a": "b", "c": "d"}),
    ],
)
def test__map_to_type__success(value, mapped_type, expected):
    assert expected == _map_to_type(value=value, type_=mapped_type)


@pytest.mark.parametrize(
    "value, mapped_type",
    [("2012-01-01", dict), ("a", int)],
)
def test__map_to_type__value_error(value, mapped_type):
    with pytest.raises(ValueError):
        _map_to_type(value=value, type_=mapped_type)
