from datetime import date
from typing import Optional

from pydantic import BaseModel
from stringcase import camelcase  # type: ignore

from app.core.monitoring import contains_phi


@contains_phi
class PatientBase(BaseModel):
    """ Properties shared among all uses """
    name: Optional[str] = None
    program: Optional[str] = None

    class Config:
        """
        Allows variables to be in snakecase, but API contracts to be in camelcase.

        (Shown as an example)
        """
        alias_generator = camelcase
        allow_population_by_field_name = True


class PatientCreate(PatientBase):
    """ Properties to receive on item creation """
    name: str  # name required on creation
    date_of_birth: date  # date of birth not allowed to be updated


class PatientUpdate(PatientBase):
    """ Properties to receive on item update """


class PatientInDBBase(PatientCreate):
    """ Properties shared by models stored in DB """
    id: int
    name: str
    date_of_birth: date

    class Config:
        orm_mode = True


class Patient(PatientInDBBase):
    """ Properties to return to client on requests """
    pass


class PatientInDB(PatientInDBBase):
    """ Additional identifying properties stored within DB """

