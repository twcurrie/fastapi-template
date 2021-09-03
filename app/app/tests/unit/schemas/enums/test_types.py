import pytest
from app.schemas.enums.types import (
    CaseInsensitiveEnum,
    CaseInsensitiveEnumWithDefault,
)


class TestEnum(CaseInsensitiveEnum):
    value_1 = "VALue_1"
    value_2 = "Value_2"
    value_3 = "VALUE_3"
    value_4 = "vaLuE_4"


@pytest.mark.parametrize(
    "provided_value, expected_return",
    [
        ("valuE_1", TestEnum.value_1),
        ("vAlUE_2", TestEnum.value_2),
        ("value_3", TestEnum.value_3),
        ("VALUE_4", TestEnum.value_4),
    ],
)
def test__case_insensitive_enum(provided_value, expected_return):
    assert TestEnum(provided_value) == expected_return


def test__case_insensitive_enum__no_default():
    with pytest.raises(ValueError):
        TestEnum("value_5")


class AnotherTestEnum(CaseInsensitiveEnumWithDefault):
    value_1 = "VALue_1"
    value_2 = "Value_2"
    unknown = "unknown"
    default = unknown


@pytest.mark.parametrize(
    "provided_value, expected_return",
    [
        ("valuE_1", AnotherTestEnum.value_1),
        ("vAlUE_2", AnotherTestEnum.value_2),
        ("UNKNOWN", AnotherTestEnum.unknown),
        ("....", AnotherTestEnum.unknown),
    ],
)
def test__case_insensitive_enum_with_default(provided_value, expected_return):
    assert AnotherTestEnum(provided_value) == expected_return
