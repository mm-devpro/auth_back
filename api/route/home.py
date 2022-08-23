from http import HTTPStatus
from werkzeug.security import check_password_hash
from flask import Blueprint, request
from flasgger import swag_from
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, unset_jwt_cookies, jwt_required


home = Blueprint('home', __name__, url_prefix="/api/v1")


@home.route('/')
@jwt_required()
def homepage():
    pass

