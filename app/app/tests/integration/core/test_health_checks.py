from app.core.health.checks import is_database_available


def test__database__health(db):
    assert is_database_available(db)
