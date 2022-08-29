from flask import Blueprint, Response
from flasgger import swag_from
from api.resource.auth import require_login
import cv2 as cv
from api.resource.camera import gen_frames

cam = Blueprint('camera', __name__, url_prefix="/api/v1")

cap = cv.VideoCapture(0)


@cam.route('/stream', methods=["GET"])
def video_feed():
    global cap
    return Response(gen_frames(cap), mimetype='multipart/x-mixed-replace; boundary=frame')
