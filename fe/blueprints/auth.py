from flask import Blueprint

authorization = Blueprint("auth", __name__, static_folder='static/')
