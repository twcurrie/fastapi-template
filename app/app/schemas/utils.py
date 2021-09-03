from datetime import date
from enum import Enum

from aenum import MultiValueEnum  # type: ignore


default_json_encoders = {
    # If using the default with overrides, ensure
    # this default is imported before any overrides, eg:
    #
    #  class Model(BaseModel):
    #     dayOfMonth: date
    #
    #     class Config:
    #         json_encoders: Mapping[Type[Any], Callable[[Any], Any]] = {
    #             **default_json_encoders,
    #             date: lambda v: v.day,
    #         }
    Enum: lambda v: v.value,
    MultiValueEnum: lambda v: v.value,
    date: lambda v: v.strftime("%Y-%m-%d"),
}
