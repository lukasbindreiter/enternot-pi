from flask import Flask

from enternot_app.auth import init_auth
from enternot_app.firebase import Firebase
from enternot_app.pi.camera import Camera


def create_app():
    app = Flask("enternot_app")
    init_auth(app)
    return app


def load_secrets(app):
    try:
        from enternot_app.secret import FIREBASE_API_KEY, BASIC_AUTH_USER, \
            BASIC_AUTH_HASHED_PW, PI_LONGITUDE, PI_LATITUDE
        app.config["FIREBASE_API_KEY"] = FIREBASE_API_KEY
        app.config["BASIC_AUTH_USER"] = BASIC_AUTH_USER
        app.config["BASIC_AUTH_HASHED_PW"] = BASIC_AUTH_HASHED_PW
        app.config["PI_LONGITUDE"] = PI_LONGITUDE
        app.config["PI_LATITUDE"] = PI_LATITUDE
    except ImportError:
        app.config["BASIC_AUTH_FORCE"] = False
        app.config["FIREBASE_API_KEY"] = None
        app.config["BASIC_AUTH_USER"] = None
        app.config["BASIC_AUTH_HASHED_PW"] = None
        app.config["PI_LONGITUDE"] = None
        app.config["PI_LATITUDE"] = None


app = create_app()
load_secrets(app)
firebase = Firebase(app)
camera = Camera(firebase)
from enternot_app import routes
