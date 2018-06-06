from flask import Flask

from enternot_app.pi.camera import Camera

app = Flask(__name__)
camera = Camera()

from enternot_app import routes
