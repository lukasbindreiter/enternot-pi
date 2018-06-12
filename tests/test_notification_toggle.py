from flask.testing import FlaskClient

from enternot_app import Camera


def test_notification_toggle(client: FlaskClient, camera: Camera):
    # test set to true
    response = client.post("/notification-toggle",
                           data='{"notifications": "true"}',
                           content_type='application/json')
    assert response.status_code == 200
    assert camera.notifications is True

    # again set to true
    response = client.post("/notification-toggle",
                           data='{"notifications": "true"}',
                           content_type='application/json')
    assert response.status_code == 200
    assert camera.notifications is True

    # set to false
    response = client.post("/notification-toggle",
                           data='{"notifications": "false"}',
                           content_type='application/json')
    assert response.status_code == 200
    assert camera.notifications is False


def test_notification_toggle_bad_requests(client: FlaskClient):
    # no body
    response = client.post("/notification-toggle")
    assert response.status_code == 400

    # invalid json
    response = client.post("/notification-toggle",
                           data='{"inv',
                           content_type='application/json')
    assert response.status_code == 400

    # wrong json key
    response = client.post("/notification-toggle",
                           data='{"wrongkey": "true"}',
                           content_type='application/json')
    assert response.status_code == 400

    # wrong value
    response = client.post("/notification-toggle",
                           data='{"notifications": "asdf"}',
                           content_type='application/json')
    assert response.status_code == 400

    # wrong value
    response = client.post("/notification-toggle",
                           data='{"notifications": [123, 456]}',
                           content_type='application/json')
    assert response.status_code == 400
