import json
from flask.testing import FlaskClient

from enternot_app import Firebase


def test_notification_toggle(client: FlaskClient, firebase: Firebase):
    # mock the _get_pi_location method:
    pi_pos = (14.320049, 48.338040)
    firebase._get_pi_location = lambda: pi_pos

    pos = dict(longitude=14.323905, latitude=48.334953)
    data = json.dumps({"location": pos})
    # test with distance of ~450m, expect notifications off
    response = client.post("/location",
                           data=data,
                           content_type='application/json')
    assert response.status_code == 200
    assert firebase.notifications is False

    # test with distance of ~22km, expect notifications on
    pos = dict(longitude=14.323218, latitude=48.135432)
    data = json.dumps({"location": pos})
    response = client.post("/location",
                           data=data,
                           content_type='application/json')
    assert response.status_code == 200
    assert firebase.notifications is True


def test_notification_toggle_bad_requests(client: FlaskClient):
    # no body
    response = client.post("/location")
    assert response.status_code == 400

    # invalid json
    response = client.post("/location",
                           data='{"inv',
                           content_type='application/json')
    assert response.status_code == 400

    # wrong json key
    response = client.post("/location",
                           data='{"wrongkey": "true"}',
                           content_type='application/json')
    assert response.status_code == 400

    # wrong value
    response = client.post("/location",
                           data='{"notifications": "asdf"}',
                           content_type='application/json')
    assert response.status_code == 400

    # wrong value
    response = client.post("/location",
                           data='{"notifications": [123, 456]}',
                           content_type='application/json')
    assert response.status_code == 400
