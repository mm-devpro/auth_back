from http import HTTPStatus
from werkzeug.security import check_password_hash
import logging
from flask import Blueprint, request, abort, make_response, jsonify
from flasgger import swag_from
from api.model.user import UserModel
from api.schema.user import user_schema, users_schema
from api.service.auth import send_token_in_cookie

from api.service.database import db

auth = Blueprint('auth', __name__, url_prefix="/api/v1")


@auth.route('/login')
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            "description": "Login Route",
            "schema": "schema to come"
        }
    }
})
def login_with_email():
    """
    Login Route
    :return:
    """
    ### 1) Check if user is in the db
    try:
        email = request.json["email"]
        user = UserModel.query.filter(UserModel.email == email).first()
        if user is None:
            logging.warning("Pas d'utilisateur correspondant")
            abort(401)

        ### 2) Check if password is good
        password = request.json["password"]
        if user.verify_password(password) is False:
            logging.warning("Error with user credentials")
            abort(401)

    except Exception as e:
        logging.warning(f"Error, {e}. Try again later")
        abort(500)
    else:
        send_token_in_cookie("user", user)


@auth.route('/signup', methods=["POST"])
def sign_up():
    """

    :return:
    """
    try:
        req = request.get_json()
        email = req["email"]
        username = req["username"]
        password = req["password"]
        user = UserModel(email=email, password=password, username=username)
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        logging.warning(e)
        abort(500)
    else:
        return jsonify({
            "status": "success",
            "statusCode": 201,
            "message": "utilisateur créé"
        })


@auth.route('/get-users', methods=["GET"])
def get_users():
    users = UserModel.query.all()
    u = users_schema.dump(users)
    return jsonify(u)

