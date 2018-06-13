from flask.testing import FlaskClient


def test_camera_feed(client: FlaskClient):
    response = client.get('/camera/stream')
    assert response.status_code == 200

