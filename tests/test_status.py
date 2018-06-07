from flask.testing import FlaskClient


def test_status(client: FlaskClient):
    response = client.get('/status')
    assert response.status_code == 200
    assert "Enternot is up and running!" in response.data.decode("utf-8")
