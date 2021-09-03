import sqlalchemy as sa

from app.db.base_class import Base
from app.db.types import phi_column as phi


class Patient(Base):
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(phi.String)
    program = sa.Column(sa.String, nullable=True)
    date_of_birth = sa.Column(phi.Date)
