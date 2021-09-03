import pytest
import sqlalchemy as sa  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.exc import IntegrityError  # type: ignore

from app.db.base_class import Base
from app.db.types import phi_column as phi


class TestUserModel(Base):
    id = sa.Column(sa.Integer, primary_key=True)
    user_name = sa.Column(phi.String(16), nullable=False)
    user_type = sa.Column(sa.String(16), nullable=False)
    user_gender = sa.Column(sa.String(16), nullable=False)


@pytest.fixture(scope="function", autouse=True)
def sample_table(db: Session):
    TestUserModel.__table__.create(db.get_bind())  # type: ignore


def test__sample_table__create_with_exception(db):
    test_user_model = TestUserModel(
        user_name="A person's name", user_type="A user type", user_gender=None
    )
    db.add(test_user_model)
    with pytest.raises(IntegrityError) as e:
        db.commit()

    assert "DETAIL" not in str(e)
    assert "A person's name" not in str(e)

    assert "A person's name" not in str(e.value.params)
    assert "A user type" in str(e.value.params)
