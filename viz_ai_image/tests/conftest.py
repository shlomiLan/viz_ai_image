import pytest

from viz_ai_image.app import app as flask_app


@pytest.fixture(scope="session", autouse=True)
def client():
    flask_client = flask_app.test_client()
    yield flask_client
