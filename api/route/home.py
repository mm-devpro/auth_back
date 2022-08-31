from http import HTTPStatus
from werkzeug.security import check_password_hash
from flask import Blueprint, request, make_response, g, jsonify
from flasgger import swag_from
from api.resource.auth import require_login

home = Blueprint('home', __name__, url_prefix="/api/v1")


@home.route('/')
# @require_login
def homepage():
    # cook = g.cookie
    # cooki = request.cookies.get("user")
    # return make_response(jsonify(cook, cooki), 200)
    return make_response(jsonify("coucou"), 200)

