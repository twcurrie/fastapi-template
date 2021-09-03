from .base import CRUDBase

from .crud_patient import patient

"""
A basic CRUD class can be created with the following:

patient = CRUDBase[Patient, PatientCreate, PatientUpdate](Patient)

"""
