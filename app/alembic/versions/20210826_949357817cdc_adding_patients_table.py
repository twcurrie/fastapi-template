"""Adding patients table

Revision ID: 949357817cdc
Revises:
Create Date: 2021-07-14 10:38:24.531353

"""
from alembic import op  # type: ignore
import sqlalchemy as sa  # type: ignore
from sqlalchemy.dialects.postgresql import UUID  # type: ignore

# revision identifiers, used by Alembic.
revision = "949357817cdc"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "patient",
        sa.Column("id", sa.Integer(), nullable=False, autoincrement=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("date_of_birth", sa.Date(), nullable=False),
        sa.Column("program", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix__patient__id"), "patient", ["id"], unique=True)


def downgrade():
    op.drop_index(op.f("ix__patient__id"), table_name="patient")
    op.drop_table("patient")
