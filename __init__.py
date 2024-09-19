from flask.app import Flask
from flask import abort, g
from flask import request, redirect, url_for, make_response
from flask.json import jsonify
import uuid
import hashlib
from . import database
import datetime
import secrets
from queue import Queue
from .login import login_blueprint
from .signup import signup_blueprint
from .home import homepage_blueprint
from .logout import logout_blueprint
from .tools import encrypt


app = Flask(__name__)
app.config['DATABASE'] = 'manaswini.db'
database.init_app(app=app)
app.secret_key = secrets.token_hex(16)
print("Secret is set")



@app.errorhandler(405)
def handleError(e):
    return jsonify({
        "code":405,
        "message":"Method not allowed"
    }), 405

@app.errorhandler(400)
def handleError(e):
    return jsonify(
        {
            "code":400,
            "message":"bad request::{}".format(str(e)),
        }
    ), 400

@app.errorhandler(404)
def handleError(e):
    return jsonify(
        {
            "code":404,
            "message":"endpoint not found."
        }
    ), 404

@app.errorhandler(500)
def handleError(e):
    return jsonify(
        {
            "code":500,
            "message":str(e),
        }
    ), 500


@app.route('/welcome', methods=('GET',))
def wishwelcome():
    return "Welcomee to the class"


app.register_blueprint(login_blueprint)
app.register_blueprint(signup_blueprint)
app.register_blueprint(homepage_blueprint)
app.register_blueprint(logout_blueprint)

if __name__ == '__main__':
    app.run(debug=True)

