from __future__ import print_function
from flask import Flask, redirect, url_for
import os
import sys
sys.path.append("../")

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("../config/local/flask.py")

    # # Import all v2 blueprints
    from .blueprints.base import base
    from .blueprints.auth import authorization

    # # Register blueprints
    app.register_blueprint(base, url_prefix='/')
    app.register_blueprint(authorization, url_prefix='/auth')

    # from .announce import anc
    # app.register_blueprint(anc,url_prefix='/')
    return app
