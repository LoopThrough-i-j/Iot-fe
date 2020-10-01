from firebase_admin import auth, exceptions
from flask import request, abort, jsonify, redirect, url_for




def extract_bearer_token(request):
    """method to extract token from the Authorization header"""
    return request.headers['Authorization'].split(" ")[-1].strip()

def verify_session_token(request):
    try:
        idToken = extract_bearer_token(request)
        return auth.verify_session_cookie(idToken, check_revoked=True)
    except:
        try:
            cookie = request.cookies.get("accessToken")
            return auth.verify_session_cookie(cookie, check_revoked=True)
        except:
            raise BaseException("Invalid access Token")

#checking and triming length
