from flask import Blueprint, request, make_response, g, jsonify
from resource.auth import require_login

home = Blueprint('home', __name__, url_prefix="/api/v1")


@home.route('/')
@require_login
def homepage():
    cook = g.cookie
    ck = request.cookies.get("user")
    return make_response(jsonify(cook, ck), 200)
