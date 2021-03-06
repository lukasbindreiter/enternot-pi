import datetime
import json

import cv2
from flask import Response, request, jsonify, render_template

from enternot_app import app, camera, firebase, speakers


@app.route("/")
@app.route("/index")
@app.route("/status")
def index():
    now = datetime.datetime.now()
    return jsonify(status="Enternot is up and running!", server_time=now)


@app.route("/camera/live")
def camera_feed():
    return Response(frame_generator(camera),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/camera/stream")
def camera_live():
    return render_template("camera.html")


@app.route("/camera/position", methods=["POST"])
def camera_position():
    try:
        data = request.json
        x_angle = None
        y_angle = None
        try:
            x_angle = data["x_angle"]
        except KeyError:
            pass

        try:
            y_angle = data["y_angle"]
        except KeyError:
            pass

        if x_angle is None and y_angle is None:
            raise ValueError("Must specify at least x or y angle")

        for angle, angle_name in [(x_angle, "x_angle"), (y_angle, "y_angle")]:
            if angle is None:
                continue
            if not isinstance(angle, (float, int)):
                raise TypeError(
                    "{} must be float or int value".format(angle_name))
            if not -180 <= angle <= 180:
                raise ValueError(
                    "{} must be between -180 and 180".format(angle_name))

        if x_angle is not None:
            camera.accumulate_angle(x_angle, 1)

        if y_angle is not None:
            camera.accumulate_angle(y_angle, 2)

        return jsonify(message="Movement initiated!")
    except (KeyError, json.JSONDecodeError, ValueError, TypeError) as err:
        response = jsonify(error=str(err))
        response.status_code = 400
        return response


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


@app.route("/siren/start", methods=["POST"])
def play_sirene():
    duration = speakers.play_siren()
    return jsonify(message="Siren playing for {} seconds!".format(duration))


@app.route("/siren/stop", methods=["POST"])
def stop_sirene():
    speakers.stop_playback()
    return jsonify(message="Siren playback stopped!")


@app.route("/audio/stream", methods=["POST"])
def play_audio_stream():
    try:
        if request.headers["Content-Type"] != "application/octet-stream":
            raise ValueError(
                "Content must be of type application/octet-stream")

        data = request.data
        speakers.play_byte_stream(data)

        return jsonify(message="Voice message is playing!")
    except (KeyError, ValueError) as err:
        response = jsonify(error=str(err))
        response.status_code = 400
        return response
