from pydantic import BaseModel

from datetime import date
from enum import Enum
from app.schemas.utils import default_json_encoders


class DummyEnum(Enum):
    RED = "red"
    YELLOW = "yellow"
    GREEN = "green"


class Model(BaseModel):
    date_of_birth: date
    an_enum: DummyEnum

    class Config:
        json_encoders = default_json_encoders


def test__default_json_encoders():
    model = Model(date_of_birth=date(year=2001, month=1, day=1), an_enum=DummyEnum.RED)
    assert model.json() == '{"date_of_birth": "2001-01-01", "an_enum": "red"}'
