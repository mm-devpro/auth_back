from http import HTTPStatus
from werkzeug.security import check_password_hash
from flask import Blueprint, request
from flasgger import swag_from
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, unset_jwt_cookies, jwt_required
from api.model.user import UserModel

auth = Blueprint('auth', __name__, url_prefix="/api/v1")


def create_token(user):
    access_token = create_access_token(identity=user.email)
    response = {"access_token": access_token}
    return response


@auth.route('/login')
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            "description": "Login Route",
            "schema": "schema to come"
        }
    }
})
def login():
    """
    Login Route
    :return:
    """
    ### 1) Check if user is in the db
    try:
        email = request.form.get("email")
        user = UserModel.query.filter(UserModel.email == email).first()
        if user is None:
            return {
                "message": "Pas d'utilisateur correspondant",
                "statusCode": 401,
                "status": "error"
            }

        ### 2) Check if password is good
        password = request.form.get("password")
        if check_password_hash(user.password, password) is False:
            return {
                "message": "Identifiants non valides, réessayez",
                "statusCode": 401,
                "status": "error"
            }
    except Exception as e:
        return {
            "message": f"Erreur, reessayer plus tard ({e})",
            "statusCode": 500,
            "status": "error"
        }
    else:
        return user.encode_auth_token()