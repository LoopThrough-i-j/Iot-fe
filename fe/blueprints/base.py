from flask import Blueprint, send_from_directory, jsonify, make_response, request
from datetime import datetime
import os

base = Blueprint("base", __name__, static_folder='static/')
