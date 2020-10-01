from datetime import datetime, timedelta
from flask import Blueprint, make_response, request
from ..utils.utils import verify_session_token, get_env
from flask_cors import CORS
import maia.utils.db as db
from firebase_admin import auth


authorization = Blueprint("auth", __name__, static_folder='/static')

CORS(authorization,
        origins="*",
        expose_headers='Authorization',
        allow_headers=[
        'Access-Control-Allow-Origin',
        'Access-Control-Allow-Methods',
        'Access-Control-Allow-Origin',
        'Authorization',
        "Access-Control-Allow-Headers",
        "Content-Type"
    ],supports_credentials=True)

@authorization.route("/token", methods=['POST'])
def token():
    """Exchanges idToken obtained at client side with server generated accessToken."""
    data = request.json
    try:
        # Get user claims from idToken generated client side
        claims = auth.verify_id_token(data['idToken'])
    except:
        # Random fail
        response = {
            "status": "fail",
            "message": "ID token verification failed"
        }
        return make_response(response, 401)

    # access token expires in 7 days
    expires_in = timedelta(days=7)
    # TIL auth.create_session_cookie() doesn't actually return a cookie
    # but the value to be put in a cookie.
    
    auth_token = auth.create_session_cookie(data['idToken'], expires_in=expires_in)

    response = {
        "status": "success",
        "accessToken": auth_token
    }

    # If sign up method is email, we have an optional userInfo field
    if data.get("userInfo"):
        user_ref = db.collection("user_profiles").document(claims['uid'])
        # If statement is not needed but anyways..
        if not user_ref.get().to_dict():
            env, isTest= get_env(request)
            companyName = data.get('companyName') if 'companyName' in data else ""
            data = {
                'userEmail': claims['email'],
                'userName': data.get('name') or claims.get('name'),
                'env': env,
                'isTest': isTest,
                'browserNotifications': False,
                'mailNotifications': True,
                'isVerified': claims['email_verified'],
                'timeStampCreated': datetime.now(),
                'lastLogin': datetime.now(),
                'credits': 10000,
                'monthlyCredits': 1000,
                'dailyCredits': 100,
                'monthlyCreditsRemaining': 1000,
                'dailyCreditsRemaining': 100,
                'isAdmin': False,
                'userCompanyName': companyName,
                'userPlan': "free",
                'isActive': True,
                'isAdmin': False
            }
            user_ref.set(data)
            response["message"] = "user created with UID: {}".format(claims['uid'])

    #return make_response(response, 200)
    res = make_response(response, 200)
    res.set_cookie('accessToken', auth_token, secure=True,httponly=True)
    
    return res


@authorization.route("/userInfo", methods=['GET', 'POST'])
def user_info():
    """Fetch and update user profile information"""
    try:
        session_data = verify_session_token(request)
    except:
        response = {
            "status": "fail",
            "message": "Invalid access token"
        }
        return make_response(response, 401)

    if request.method == "GET":
        # support ?refresh=True switch to control whether firebase read
        # happends or not.
        user_profile = db.collection("user_profiles").document(session_data['uid']).get().to_dict()
        user_profile['uid'] = session_data['uid']
        return user_profile

    if request.method == "POST":
        data = request.json
        try:
            db.collection("user_profiles").document(session_data['uid']).update(data)
        except:
            response = {
                "status": "fail",
                "message": "error while updating data"
            }
            return make_response(response, 400)

        response = {
            "status": "success",
            "message": "user profile updated successfuly"
        }
        return make_response(response, 200)

@authorization.route("/removeCookie", methods=['GET'])
def remCookie():
    resp = make_response(
        {
            "status":"success"
        }, 200)
    resp.set_cookie('accessToken', '', 
        secure=True, httponly=True, samesite="Strict")
    return resp
