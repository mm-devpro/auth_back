from flask import Blueprint, Response, g, abort
from flasgger import swag_from
from api.resource.auth import require_login
import cv2 as cv
from api.resource.camera import Camera
from api.resource.webcam_stream import WebcamStream

cam = Blueprint('camera', __name__, url_prefix="/api/v1")


@cam.route('/stream/<camera_url>/', methods=["GET"])
def video_feed(camera_url):
    camera = Camera(camera_url)
    # webcam = WebcamStream(stream_id=camera_url)

    return Response(camera.get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')
