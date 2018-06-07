import pytest

from enternot_app import app as flask_app


@pytest.fixture(scope='session')
def app(request):
    app = flask_app
    app.config["DEBUG"] = True
    app.config["TESTING"] = True

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)

    return app


@pytest.fixture()
def myfixture():
    return "this is my fixture!!"