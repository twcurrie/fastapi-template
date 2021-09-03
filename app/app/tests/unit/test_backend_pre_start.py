import pytest
from mock import MagicMock, Mock

import logging
from tenacity import RetryError


def test__main__exception_thrown(caplog, monkeypatch):
    monkeypatch.setenv("DB_STARTUP_MAX_ATTEMPTS", "1")

    from app.backend_pre_start import main

    expected_message = "This is expected"

    mock_session = MagicMock()
    mock_session.execute = Mock(side_effect=ValueError(expected_message))

    caplog.clear()
    caplog.set_level(logging.DEBUG)
    with pytest.raises(RetryError):
        main(mock_session)

    mock_session.execute.assert_called_once_with("SELECT 1")
    assert expected_message in [record.message for record in caplog.records]


def test__main__success(caplog, monkeypatch):
    monkeypatch.setenv("DB_STARTUP_MAX_ATTEMPTS", "1")

    from app.backend_pre_start import main

    mock_session = MagicMock()
    mock_session.execute = Mock(return_value=None)

    caplog.clear()
    caplog.set_level(logging.DEBUG)
    main(mock_session)

    mock_session.execute.assert_called_once_with("SELECT 1")
    assert "Service finished initializing" in [
        record.message for record in caplog.records
    ]
