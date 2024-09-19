from flask import Blueprint, render_template,make_response, redirect, url_for
from flask.app import session, request
from flask.json import jsonify
from flask.sessions import SessionMixin
from . import database

logout_blueprint = Blueprint('logout', __name__)

@logout_blueprint.route('/auth/logout', methods=['POST'])
def userLogout():
    base = database.get_db()
    cursor = base.cursor()
    session.clear()
    sessionId = request.cookies.get('userSession')
    response_data = {'success':0, 'message':''}
    if (not sessionId) :
        response_data['message'] = 'To logout you have to login first.'
        response_data['success'] = 1
        return make_response(jsonify(response_data))
    
    SESSION_QUERY = "DELETE FROM sessionCookies where cookieId=?"
    cursor.execute(SESSION_QUERY, (sessionId,))

    base.commit()


    response = make_response(
        jsonify(
            {
                "success":1,
                "message":"Logout Successful",
            }
        )
    )

    response.set_cookie("userSession", sessionId, expires=0)

    return response,201
