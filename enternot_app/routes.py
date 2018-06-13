import datetime
import json

import cv2
from flask import Response, request, jsonify

from enternot_app import app, camera, firebase


@app.route("/")
@app.route("/index")
@app.route("/status")
def index():
    now = datetime.datetime.now()
    return jsonify(status="Enternot is up and running!", server_time=now)


@app.route("/camera/stream")
def camera_feed():
    return Response(frame_generator(camera),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


def frame_generator(camera):
    while True:
        frame = cv2.imencode(".jpg", camera.frame)[1].tobytes()

        new_line = b"\r\n"
        frame_separator = b"--frame"
        frame_packet = b"Content-Type: image/jpeg"

        yield frame_separator + new_line + frame_packet + new_line + new_line + frame + new_line

        camera.wait_for_next_frame()


@app.route("/notification-toggle", methods=["POST"])
def notification_toggle():
    """
    Endpoint to toggle the sending of push notifications upon movement detected

    Expects POST request in the form of:
    {'notifications': 'true'}
    where the value can either be 'true' or 'false'

    Returns:

    """
    try:
        data = request.json
        send_notifications = json.loads(data["notifications"])
        if not isinstance(send_notifications, bool):
            raise ValueError()

        firebase.notifications = send_notifications
        return jsonify(notifications=firebase.notifications)
    except (KeyError, json.JSONDecodeError, ValueError, TypeError):
        return Response(status=400)  # Bad Request
