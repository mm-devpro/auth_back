import os
import logging
import jwt
from flask import abort, request, g


def decode_cookie():
    """
    Function to decode cookie and set our api global "cookie" variable with
    what is found in the cookie
    """
    cookie = request.cookies.get("user")

    if not cookie:
        g.cookie = {}
        return

    try:
        g.cookie = jwt.decode(cookie, os.environ["SECRET_KEY"], algorithms=["HS256"])
    except jwt.InvalidTokenError as err:
        logging.warning(str(err))
        abort(401)
