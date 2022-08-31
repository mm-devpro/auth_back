from flask import Blueprint, Response, g, abort
from flasgger import swag_from
from api.resource.auth import require_login
import cv2 as cv
from api.resource.camera import Camera

cam = Blueprint('camera', __name__, url_prefix="/api/v1")


@cam.route('/stream/<camera_url>/', methods=["GET"])
def video_feed(camera_url):
    camera = Camera(camera_url)
    return Response(camera.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
