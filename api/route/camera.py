from flask import Blueprint, Response
from flasgger import swag_from
from api.resource.auth import require_login
import threading
import cv2 as cv

cam = Blueprint('camera', __name__, url_prefix="/api/v1")

lock = threading.Lock()


@cam.route('/stream', methods=["GET"])
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def gen_frames():
    global lock

    cap = cv.VideoCapture(0)
    if cap.isOpened():
        success, frame = cap.read()
    else:
        success = False

    # while True, so it's streaming
    while success:
        # wait until the lock is acquired
        with lock:
            # read the next frame
            success, frame = cap.read()
            # if blank frame
            if frame is None:
                continue

            # encode the frame to JPEG format
            ret, buffer = cv.imencode('.jpg', frame)
            # ensure the frame was successfully encoded
            if not ret:
                continue

        #yield the output frame in the byte format
        yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(buffer) + b'\r\n'

    cap.release()
