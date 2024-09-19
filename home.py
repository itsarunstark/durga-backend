from flask import Flask, jsonify, url_for, redirect, render_template, request, make_response
from flask.blueprints import Blueprint
import datetime
import uuid
from . import database
homepage_blueprint = Blueprint('home', __name__)

@homepage_blueprint.route('/')
def homepage():
    base = database.get_db()
    cursor = base.cursor()
    sessionId = request.cookies.get('userSession')
    if (not sessionId):
        return jsonify([
            {
                "code":"403",
                "message":"forbidden, you need to login first"
            }
        ]), 403
    
    SESSION_QUERY = "SELECT s1.userId, s1.created, s1.expiry, u1.username \
        FROM sessionCookies s1 INNER JOIN user u1 \
        ON u1.userId = s1.userId WHERE s1.cookieId = ?"
    print(sessionId)
    cursor.execute(SESSION_QUERY, (sessionId,))
    sessionInfo = cursor.fetchone()
    if not sessionInfo:
        response = make_response(
            jsonify(
                {'code':404, 'message':'user not found please re-login'}
            )
        )
        response.set_cookie('userSession', sessionId, expires=0)
        return response, 404
    print(list(sessionInfo))
    userId, creationDate, expiryDate, username = sessionInfo
    currentTime = datetime.datetime.now()
    print(expiryDate, currentTime)
    if (currentTime > expiryDate) :
        response = make_response(
            jsonify(
                {"code":403, "message":"Session has been expired please re-login"}
            )
        )
        response.set_cookie('userSession', sessionId, expires=0)
        return response, 403
    return jsonify(
        {
            "code":200,
            "message":"welcome back {}".format(username)
        }
    )