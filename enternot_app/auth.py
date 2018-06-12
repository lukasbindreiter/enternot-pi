import os
from flask_basicauth import BasicAuth
from flask import current_app
import hashlib


class BcryptBasicAuth(BasicAuth):
    def check_credentials(self, username, password):
        """
        Check if the given username and password are correct.
        """
        correct_username = current_app.config['BASIC_AUTH_USERNAME']
        correct_password_hash = current_app.config['BASIC_AUTH_PASSWORD_HASH']

        md5 = hashlib.md5()
        md5.update(password.encode("ascii"))
        hash = md5.hexdigest()

        return username == correct_username and correct_password_hash == hash


def init_auth(app):
    try:
        from enternot_app.secret import BASIC_AUTH_USER, BASIC_AUTH_HASHED_PW
    except ImportError:
        BASIC_AUTH_USER = os.getenv("ENTERNOT_BASIC_AUTH_USER")
        BASIC_AUTH_HASHED_PW = os.getenv("ENTERNOT_BASIC_AUTH_HASHED_PW").encode("ascii")

    if BASIC_AUTH_USER is None or BASIC_AUTH_HASHED_PW is None:
        print("Warning: Basic Auth username or password not found. Basic Auth will be disabled")
    else:
        app.config["BASIC_AUTH_USERNAME"] = BASIC_AUTH_USER
        app.config["BASIC_AUTH_PASSWORD_HASH"] = BASIC_AUTH_HASHED_PW
        app.config["BASIC_AUTH_FORCE"] = True
        basic_auth = BcryptBasicAuth(app)
