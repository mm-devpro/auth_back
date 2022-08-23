from datetime import timedelta
from flask import jsonify, request
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, unset_jwt_cookies, jwt_required

from api.model.user import UserModel


def create_token(user):
    additional_claims = {"username": user.username}
    access_token = create_access_token(
        identity=user.email,
        expires_delta=timedelta(days=30),
        additional_claims=additional_claims)
    return jsonify(access_token=access_token)


def get_user():
    ### 1) Check if user is in the db
    try:
        email = request.form.get("email")
        user = UserModel.query.filter(UserModel.email == email).first()
        if user is None:
            return jsonify(
                message="Pas d'utilisateur correspondant",
                statusCode=401,
                status="error"
            )

        ### 2) Check if password is good
        password = request.form.get("password")
        if check_password_hash(user.password, password) is False:
            return jsonify(
                message="Identifiants non valides, réessayez",
                statusCode=401,
                status="error"
            )
    except Exception as e:
        return jsonify(
            message=f"Erreur, reessayer plus tard ({e})",
            statusCode=500,
            status="error"
        )
    else:
        return jsonify(
            user=user,
            status="success",
            statusCode=200
        )
