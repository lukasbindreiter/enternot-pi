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


@app.route("/camera/position", methods=["POST"])
def camera_position():
    try:
        data = request.json
        angle = data["angle"]
        if not isinstance(angle, (float, int)):
            raise TypeError()
        if not 0 <= angle <= 360:
            raise ValueError()

        camera.accumulate_angle(angle, 1)
        print("move to angle {:d}".format(angle))

        return Response(status=200)
    except (KeyError, json.JSONDecodeError, ValueError, TypeError) as err:
        return Response(status=400)  # Bad Request


def frame_generator(camera):
    while True:
        frame = cv2.imencode(".jpg", camera.frame)[1].tobytes()

        new_line = b"\r\n"
        frame_separator = b"--frame"
        frame_packet = b"Content-Type: image/jpeg"

        yield frame_separator + new_line + frame_packet + new_line + new_line + frame + new_line

        camera.wait_for_next_frame()


@app.route("/location", methods=["POST"])
def update_location():
    """
    Endpoint to update the pi about a users location. Based on this data,
    push notifications will be turned off.
    """
    try:
        data = request.json
        user_lon = data["location"]["longitude"]
        user_lat = data["location"]["latitude"]
        if not isinstance(user_lon, float) or not isinstance(user_lat, float):
            raise TypeError()

        distance = firebase.toggle_notifications_based_on_distance(user_lon,
                                                                   user_lat)

        return jsonify(notifications=firebase.notifications, distance=distance)
    except (KeyError, json.JSONDecodeError, ValueError, TypeError):
        return Response(status=400)  # Bad Request
