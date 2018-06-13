import hashlib

from flask import current_app
from flask_basicauth import BasicAuth


class BcryptBasicAuth(BasicAuth):
    def check_credentials(self, username, password):
        """
        Check if the given username and password are correct.
        """
        correct_username = current_app.config['BASIC_AUTH_USER']
        correct_password_hash = current_app.config['BASIC_AUTH_HASHED_PW']

        # check if basic auth is enabled:
        if correct_username is None and correct_password_hash is None:
            return True

        md5 = hashlib.md5()
        md5.update(password.encode("ascii"))
        hash = md5.hexdigest()

        return username == correct_username and correct_password_hash == hash


def init_auth(app):
    app.config["BASIC_AUTH_FORCE"] = True
    BcryptBasicAuth(app)
