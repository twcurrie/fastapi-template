import logging

from app.core.environment import Environment


def test__environment__override(caplog):
    unknown_environment = "unknown"
    caplog.clear()
    caplog.set_level(logging.DEBUG)
    environment = Environment(unknown_environment)

    assert environment.value == Environment.DEVELOPMENT.value
    expected_message = f"Unknown environment string provided ({unknown_environment}), defaulting to DEVELOPMENT"
    assert expected_message in [record.message for record in caplog.records]


def test__environment__is_production():
    assert not Environment("dev").is_production()
    assert Environment("prod").is_production()
    assert Environment("PROD").is_production()
    assert Environment("production").is_production()


def test__environment__is_testing():
    assert not Environment("prod").is_testing()
    assert Environment("test").is_testing()
    assert Environment("TEST").is_testing()
    assert Environment("testing").is_testing()
