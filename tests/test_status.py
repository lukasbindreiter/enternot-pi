from flask.testing import FlaskClient


def test_status(client: FlaskClient):
    response = client.get('/status')
    assert response.status_code == 200
    assert "status" in response.json
    assert "server_time" in response.json
