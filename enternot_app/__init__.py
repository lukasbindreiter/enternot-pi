from flask import Flask

from enternot_app.auth import init_auth
from enternot_app.firebase import Firebase
from enternot_app.pi.camera import Camera


def create_app():
    app = Flask("enternot_app")
    init_auth(app)
    return app


app = create_app()
firebase = Firebase()
camera = Camera(firebase)
from enternot_app import routes
