from flask.app import Flask
from flask.blueprints import Blueprint
from flask.json import jsonify
from flask import request, url_for
import uuid
from .tools import encrypt
from . import database

signup_blueprint = Blueprint('signup', __name__)

@signup_blueprint.route('/auth/signup', methods=('POST',))
def signup():
    base = database.get_db()
    cursor = base.cursor()
    userdata:dict = request.get_json()
    print("data", userdata)
    if not ('username' in userdata \
        and 'password' in userdata \
        and 'aadhar' in userdata \
        and 'phone' in userdata
    ):

        abort(400, description="request lacks suffcient data CODE::ERR_NOT_COMPLETE_DATA")
    
    cursor.execute("SELECT LOWER(username), aadhar FROM user WHERE username=? OR aadhar=?", (userdata['username'].lower(), userdata['aadhar']))
    current_data = cursor.fetchone()
    if (current_data):
        if (current_data[0] == userdata['username']):
            return jsonify(
                {
                    "success":0,
                    "message":"username is in use",
                }
            ), 400

        if (current_data[1] == userdata['aadhar']):
            return jsonify(
                {
                    "success":0,
                    "message":"aadhar is in use",
                }
            )

    cursor.execute(
        "INSERT INTO user(userId, username, userpass, aadhar, profileUrl) VALUES(?, ?, ?, ?, ?)",
        (
            str(uuid.uuid1()),
            userdata['username'].lower(),
            encrypt(userdata['password']),
            userdata['aadhar'],
            "https://i.imgur.com/NUyttbnb.jpg",
        )
    )
    
    base.commit()

    return jsonify(
        {
            "success":1,
            "message":"user registered successfully.",
        }
    )