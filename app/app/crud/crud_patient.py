from sqlalchemy.orm import Session  # type: ignore

from app.crud.base import CRUDBase
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate


class CRUDPatient(CRUDBase[Patient, PatientCreate, PatientUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Patient:
        return db.query(self.model).filter(Patient.name == name).first()


patient = CRUDPatient(Patient)
