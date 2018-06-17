import json

from flask.testing import FlaskClient


def test_camera_position(client: FlaskClient):
    data = json.dumps({"x-angle": 12.5})
    response = client.post("/camera/position",
                           data=data,
                           content_type='application/json')
    assert response.status_code == 200

    data = json.dumps({"y-angle": 180})
    response = client.post("/camera/position",
                           data=data,
                           content_type='application/json')
    assert response.status_code == 200

    data = json.dumps({"x-angle": 12.5, "y-angle": -180})
    response = client.post("/camera/position",
                           data=data,
                           content_type='application/json')
    assert response.status_code == 200


def camera_position_bad_requests(client: FlaskClient):
    # no body
    response = client.post("/camera/position")
    assert response.status_code == 400

    # invalid json
    response = client.post("/camera/position",
                           data='{"inv',
                           content_type='application/json')
    assert response.status_code == 400

    # wrong json key
    response = client.post("/camera/position",
                           data='{"wrongkey": "true"}',
                           content_type='application/json')
    assert response.status_code == 400

    # wrong value type
    response = client.post("/camera/position",
                           data='{"angle": "asdf"}',
                           content_type='application/json')

    # invalid angle values
    data = json.dumps({"x-angle": -190})
    response = client.post("/camera/position",
                           data=data,
                           content_type='application/json')
    assert response.status_code == 400

    data = json.dumps({"y-angle": 190})
    response = client.post("/camera/position",
                           data=data,
                           content_type='application/json')
    assert response.status_code == 400
