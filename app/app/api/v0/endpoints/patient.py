from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session  # type: ignore

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Patient])
def get_patients(
    db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100,
) -> Any:
    """
    Retrieve patients.
    """
    return crud.patient.get_multi(db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.Patient)
def create_patient(
    *, db: Session = Depends(deps.get_db), patient_in: schemas.PatientCreate,
) -> Any:
    """
    Create new patient.
    """
    patient = crud.patient.create(db=db, obj_in=patient_in)
    return patient


@router.put("/{id}", response_model=schemas.Patient)
def update_patient(
    *, db: Session = Depends(deps.get_db), id: int, patient_in: schemas.PatientUpdate,
) -> Any:
    """
    Update a patient.
    """
    patient = crud.patient.get(db=db, id=id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    patient = crud.patient.update(db=db, db_obj=patient, obj_in=patient_in)
    return patient


@router.get("/{id}", response_model=schemas.Patient)
def read_patient(*, db: Session = Depends(deps.get_db), id: int,) -> Any:
    """
    Get patient by ID.
    """
    patient = crud.patient.get(db=db, id=id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.delete("/{id}", response_model=schemas.Patient)
def delete_patient(*, db: Session = Depends(deps.get_db), id: int,) -> Any:
    """
    Delete a patient.
    """
    patient = crud.patient.get(db=db, id=id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    patient = crud.patient.remove(db=db, id=id)
    return patient
