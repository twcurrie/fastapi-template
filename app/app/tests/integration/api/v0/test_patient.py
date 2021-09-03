import random
from datetime import date
from typing import Callable

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate


def test__create_patient(
    client: TestClient,
    basic_auth_headers: dict,
    db: Session,
    random_name: str,
    random_date: date,
) -> None:
    data = {"name": random_name, "dateOfBirth": random_date, "program": "chronic knee"}
    r = client.post(
        f"{settings.API_V0_STR}/patients/", headers=basic_auth_headers, json=data,
    )
    assert 200 <= r.status_code < 300
    created_user = r.json()
    patient = crud.patient.get_by_name(db, name=random_name)

    assert patient.name == created_user["name"]
    assert patient.program == created_user["program"]
    assert str(patient.date_of_birth) == created_user["dateOfBirth"]


def test__get_patient(
    client: TestClient,
    basic_auth_headers: dict,
    db: Session,
    random_name: str,
    random_date: date,
) -> None:
    patient_in = PatientCreate(
        name=random_name, date_of_birth=random_date, program="chronic-knee"
    )
    patient = crud.patient.create(db, obj_in=patient_in)
    patient_id = patient.id
    r = client.get(
        f"{settings.API_V0_STR}/patients/{patient_id}", headers=basic_auth_headers,
    )
    assert 200 <= r.status_code < 300

    api_patient = r.json()
    existing_patient = crud.patient.get_by_name(db, name=random_name)

    assert existing_patient
    assert existing_patient.name == api_patient["name"]
    assert existing_patient.program == api_patient["program"]
    assert str(existing_patient.date_of_birth) == api_patient["dateOfBirth"]


def test__get_patient__unknown(
    client: TestClient,
    basic_auth_headers: dict,
    db: Session,
    random_name: str,
    random_date: date,
) -> None:
    patient_id = random.choice(range(0, 100))
    r = client.get(
        f"{settings.API_V0_STR}/patients/{patient_id}", headers=basic_auth_headers,
    )
    assert r.status_code == 404


def test__get_patients(
    client: TestClient,
    basic_auth_headers: dict,
    db: Session,
    get_random_name: Callable[[], str],
    get_random_date: Callable[[], date],
    random_date: date,
) -> None:
    def create_patient() -> Patient:
        patient_in = PatientCreate(
            name=get_random_name(),
            date_of_birth=get_random_date(),
            program="chronic-knee",
        )
        return crud.patient.create(db, obj_in=patient_in).id

    existing_patients = [create_patient() for _ in range(0, 4)]

    r = client.get(f"{settings.API_V0_STR}/patients/", headers=basic_auth_headers)
    assert 200 <= r.status_code < 300

    all_patients = r.json()

    assert len(all_patients) == len(existing_patients)
    for patient in all_patients:
        assert patient["id"] in existing_patients


def test__delete_patient(
    client: TestClient,
    basic_auth_headers: dict,
    db: Session,
    random_name: str,
    random_date: date,
) -> None:
    patient_in = PatientCreate(
        name=random_name, date_of_birth=random_date, program="chronic-knee"
    )
    created_patient = crud.patient.create(db, obj_in=patient_in)
    patient_id = created_patient.id
    r = client.delete(
        f"{settings.API_V0_STR}/patients/{patient_id}", headers=basic_auth_headers,
    )
    assert 200 <= r.status_code < 300

    deleted_patient = r.json()

    patient = crud.patient.get(db, id=deleted_patient["id"])

    assert not patient
    assert deleted_patient["name"] == created_patient.name
    assert deleted_patient["program"] == created_patient.program
    assert deleted_patient["dateOfBirth"] == str(created_patient.date_of_birth)


def test__delete_patient__unknown(
    client: TestClient,
    basic_auth_headers: dict,
    db: Session,
    random_name: str,
    random_date: date,
) -> None:
    patient_id = random.choice(range(0, 100))
    r = client.delete(
        f"{settings.API_V0_STR}/patients/{patient_id}", headers=basic_auth_headers,
    )
    assert r.status_code == 404


def test__update_patient(
    client: TestClient,
    basic_auth_headers: dict,
    db: Session,
    random_name: str,
    random_date: date,
) -> None:
    patient_in = PatientCreate(
        name=random_name, date_of_birth=random_date, program="chronic-knee"
    )
    created_patient = crud.patient.create(db, obj_in=patient_in)
    patient_id = created_patient.id

    data = {"program": "chronic elbow"}
    r = client.put(
        f"{settings.API_V0_STR}/patients/{patient_id}",
        headers=basic_auth_headers,
        json=data,
    )
    assert 200 <= r.status_code < 300

    api_patient = r.json()
    updated_patient = crud.patient.get(db, id=patient_id)

    assert updated_patient.name == api_patient["name"]
    assert str(updated_patient.date_of_birth) == api_patient["dateOfBirth"]

    assert api_patient["program"] != patient_in.program
    assert updated_patient.program == api_patient["program"]


def test__updated_patient__unknown(
    client: TestClient,
    basic_auth_headers: dict,
    db: Session,
    random_name: str,
    random_date: date,
) -> None:
    patient_id = random.choice(range(0, 100))
    data = {"program": "chronic elbow"}
    r = client.put(
        f"{settings.API_V0_STR}/patients/{patient_id}",
        headers=basic_auth_headers,
        json=data,
    )
    assert r.status_code == 404
