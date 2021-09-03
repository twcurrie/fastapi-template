from sqlalchemy.orm import Session  # type: ignore

from datetime import date

from app import crud
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate


def test__create_patient(db: Session) -> None:
    new_patient = PatientCreate(
        program="chronic-knee",
        name="A Patient",
        date_of_birth=date(year=2000, month=1, day=1)
    )
    patient: Patient = crud.patient.create(db, obj_in=new_patient)

    assert patient.program == new_patient.program
    assert patient.name == new_patient.name
    assert patient.date_of_birth == new_patient.date_of_birth


def test__update_patient(db: Session) -> None:
    initial_patient = PatientCreate(
        program="chronic-knee",
        name="A Patient",
        date_of_birth=date(year=2000, month=1, day=1)
    )
    patient: Patient = crud.patient.create(db, obj_in=initial_patient)

    updates = PatientUpdate(program="chronic-elbow")
    updated_patient: Patient = crud.patient.update(db, db_obj=patient, obj_in=updates)

    assert patient.name == updated_patient.name
    assert patient.date_of_birth == updated_patient.date_of_birth

    assert patient.program == updates.program


def test__get_patient(db: Session) -> None:
    new_patient = PatientCreate(
        program="chronic-knee",
        name="A Patient",
        date_of_birth=date(year=2000, month=1, day=1)
    )
    patient: Patient = crud.patient.create(db, obj_in=new_patient)

    stored_patient = crud.patient.get(db, id=patient.id)

    assert stored_patient
    assert patient.program == stored_patient.program
    assert patient.name == stored_patient.name
    assert patient.date_of_birth == stored_patient.date_of_birth


def test__delete_patient(db: Session) -> None:
    new_patient = PatientCreate(
        program="chronic-knee",
        name="A Patient",
        date_of_birth=date(year=2000, month=1, day=1)
    )
    patient: Patient = crud.patient.create(db, obj_in=new_patient)

    deleted_patient: Patient = crud.patient.remove(db, id=patient.id)

    stored_patient = crud.patient.get(db, id=patient.id)
    assert stored_patient is None

    assert patient.name == deleted_patient.name
    assert patient.program == deleted_patient.program
    assert patient.date_of_birth == deleted_patient.date_of_birth
