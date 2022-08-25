import os
import logging
import jwt
from datetime import timedelta
from flask import abort, jsonify, request, g, make_response
from werkzeug.security import check_password_hash


def decode_cookie():
    cookie = request.cookies.get("user")

    if not cookie:
        g.cookie = {}
        return

    try:
        g.cookie = jwt.decode(cookie, os.environ["SECRET_KEY"], algorithms=["HS256"])
    except jwt.InvalidTokenError as err:
        logging.warning(str(err))
        abort(401)


def send_token_in_cookie(token_name, token):
    response = make_response(200, "")
    response.set_cookie(token_name, token)
    return response
