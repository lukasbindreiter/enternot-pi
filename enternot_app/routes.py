from flask import Response
import datetime
import time
import cv2

from enternot_app import app, camera


@app.route("/")
@app.route("/index")
@app.route("/status")
def index():
    now = datetime.datetime.now()
    return "Enternot is up and running! Current server time: {}".format(now)


@app.route("/camera-feed")
def camera_feed():
    return Response(frame_generator(camera),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


def frame_generator(camera):
    while True:
        print("Next frame")
        camera.capture_frame()
        frame = cv2.imencode(".jpg", camera.get_current_frame())[1].tobytes()

        new_line = b"\r\n"
        frame_separator = b"--frame"
        frame_packet = b"Content-Type: image/jpeg"

        yield frame_separator + new_line + frame_packet + new_line + new_line + frame + new_line

        time.sleep(0.5)
