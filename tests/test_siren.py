from flask.testing import FlaskClient
import time

from enternot_app import Speakers


def test_start(client: FlaskClient, speakers: Speakers):
    # don't want to hear audio during testing
    speakers._audio_device = False
    
    response = client.post('/siren/start')
    assert response.status_code == 200
    time.sleep(1)

    response = client.post('/siren/stop')
    assert response.status_code == 200
