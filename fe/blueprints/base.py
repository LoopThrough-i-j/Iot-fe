from flask import Blueprint

from flask import Blueprint, send_from_directory, jsonify, make_response, request
from firebase_admin import firestore,credentials, initialize_app, auth, storage
from .utils.utils import verify_session_token, get_env
from datetime import datetime
import os

base = Blueprint("base", __name__, static_folder='static/')

@base.route("/preferences", methods=['GET', 'POST'])
def preferences():
    """Endpoint to play with user preferences"""
    

    if request.method == "GET":
        try:
            session_data = verify_session_token(request)
        except:
            response = {
                "status": "fail",
                "message": "token verification failed"
            }
            return make_response(response, 403)

        user_ref = db.collection("user_profiles").document(session_data['uid'])
        user = user_ref.get().to_dict()

        preferences = {
            "BrowserNotifications": user.get('BrowserNotifications'),
            "MailNotifications": user.get('MailNotifications'),
            "MailVerified": session_data.get('email_verified'),
            "name": user.get('name'),
            "Email": user.get('email')
        }
        return make_response(preferences, 200)

    if request.method == "POST":
        data = request.json
        # print(data)
        if all(pref in list(preferences.keys()) for pref in list(data.keys())):
            preferences.update(data)
            user_ref.update(preferences)

            response = {
                "status": "success",
                "message": "preferences updated successfully"
            }
            return make_response(response, 200)


@base.route("/isLogged",methods = ['GET'])
def isSignedIn():
    cookie = request.cookies.get('accessToken')
    try:
        session_data = auth.verify_session_cookie(cookie, check_revoked=True)
        return make_response({
            "response": True,
        },200)
    except:
        return make_response({
            "response": False,
        },200)