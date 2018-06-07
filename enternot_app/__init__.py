from flask import Flask

from enternot_app.pi.camera import Camera


def create_app():
    app = Flask("enternot_app")
    return app


app = create_app()
camera = Camera()
from enternot_app import routes
