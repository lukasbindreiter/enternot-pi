import pytest

from enternot_app import app as _app
from enternot_app import camera as _camera
from enternot_app import firebase as _firebase


@pytest.fixture(scope="session")
def app(request):
    _app.config["DEBUG"] = True
    _app.config["TESTING"] = True
    # disable authentication for tests
    _app.config["BASIC_AUTH_FORCE"] = False

    # Establish an application context before running the tests.
    ctx = _app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)

    return _app


@pytest.fixture(scope="session")
def camera():
    return _camera


@pytest.fixture(scope="session")
def firebase():
    return _firebase
