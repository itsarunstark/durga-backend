from flask import Blueprint, request, jsonify, redirect, url_for, make_response
import datetime
import uuid
import hashlib
from . import database
from .tools import encrypt


login_blueprint = Blueprint('login', __name__)

@login_blueprint.route('/session/verify')
def verifySession():
    sessionCookie = str(uuid.uuid1())
    base = database.get_db()
    cursor = base.cursor()

    response = make_response(
            redirect(url_for('home.homepage'))
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
    # print(request.headers.get('user-agent'))
    device_id = '{}:{}'.format(request.remote_addr, request.headers.get('user-agent'))
    unique_id = hashlib.sha256(device_id.encode('utf-8')).hexdigest()
    # response.content_type = 'application/json'

    QUERY_STRING = "INSERT INTO sessionCookies(cookieId, userId, expiry, created, deviceId) VALUES(?, ?, ?, ?, ?)"

    cursor.execute(
        QUERY_STRING,
        (sessionCookie, userId, expireDate, created, unique_id)
    )

    base.commit()
    response.set_cookie('userSession', sessionCookie, expires=expireDate.timestamp())
    return response, 302

@login_blueprint.route('/auth/login', methods=('POST',))
def loginSession():
    base = database.get_db()
    cursor = base.cursor()
    userdata:dict = request.get_json()
    DELETE_REQUEST = "DELETE FROM sessionCookies WHERE cookieId=?"

    sessionId = request.cookies.get('userSession')
    print(sessionId)

    if not ('identifier' in userdata and 'password' in userdata):
        return jsonify(
            {
                "success":0,
                "message":"Lacks sufficient data"
            }
        ), 400;
    
    if (sessionId):
        print("EXECUTING QURY NOW!!")
        cursor.execute(DELETE_REQUEST, (sessionId,))
        base.commit()

    QUERY_STRING = "SELECT userId, LOWER(username), userpass, aadhar FROM user WHERE username=? OR aadhar=?"
    cursor.execute(QUERY_STRING, (userdata.get('identifier'),userdata.get('identifier')))
    userinfo = cursor.fetchone()
    if not userinfo:
        return jsonify(
            {
                "success":0,
                "message":"username or aadhar is wrong;no user found"
            }
        )
    userId, username, userpass, aadhar = userinfo
    if ( 
        (username == userdata.get('identifier') or aadhar == str(userdata.get('identifier')))
         and encrypt(userdata.get('password')) == userpass):
         return redirect(url_for('login.verifySession', userId=userId)), 301


    return jsonify(
        {
            "success":0,
            "message":"Wrong Credidentials",
        }
    ), 401
    