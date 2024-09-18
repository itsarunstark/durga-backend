from flask import Blueprint, request, jsonify, redirect, url_for, make_response
import datetime
import uuid
import hashlib
from . import database


login_blueprint = Blueprint('login', __name__)

@login_blueprint.route('/session/verify')
def verifySession():
    sessionCookie = str(uuid.uuid1())
    base = database.get_db()
    cursor = base.cursor()

    response = make_response(
            jsonify({
                "success":1,
                "message":"Login Cookie generated",
            })
        )
    userId = request.args.get('userId')
    if (not userId):
        return jsonify(
            {
                "success":0,
                "message":"Error cannot generate session cookie as redirection is failed.",
            }
        ), 401
    created = datetime.datetime.now()
    expireDate = datetime.datetime.now() + datetime.timedelta(days=90)
    print(request.headers.get('user-agent'))
    device_id = '{}:{}'.format(request.remote_addr, request.headers.get('user-agent'))
    unique_id = hashlib.sha256(device_id.encode('utf-8')).hexdigest()
    response.content_type = 'application/json'

    QUERY_STRING = "INSERT INTO sessionCookies(cookieId, userId, expiry, created, deviceId) VALUES(?, ?, ?, ?, ?)"

    cursor.execute(
        QUERY_STRING,
        (sessionCookie, userId, expireDate, created, unique_id)
    )

    base.commit()

    response.set_cookie('userSession', sessionCookie, expires=expireDate.timestamp())
    return response,200

@login_blueprint.route('/auth/login', methods=('POST',))
def loginSession():
    base = database.get_db()
    cursor = base.cursor()
    userdata:dict = request.get_json()
    if not ('identifier' in userdata and 'password' in userdata):
        return jsonify(
            {
                "success":0,
                "message":"Lacks sufficient data"
            }
        ), 400;
    
    QUERY_STRING = "SELECT * FROM user WHERE username=? OR aadhar=?"
    cursor.execute(QUERY_STRING, (userdata.get('identifier'),userdata.get('identifier')))
    user= cursor.fetchone()
    if not user:
        return jsonify(
            {
                "success":0,
                "message":"username or aadhar is wrong and not found"
            }
        )
    userId = user[0]

    return redirect(url_for('login.verifySession', userId=userId)), 301
    