import pytest

from explorer import app


@pytest.fixture()
def mock_app():
    app.config.update(
        {
            "TESTING": True,
        }
    )
    yield app


@pytest.fixture()
def client(mock_app):
    return mock_app.test_client()
