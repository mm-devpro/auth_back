import cv2 as cv


class Camera:

    def __init__(self, camera_url):
        self.url = int(camera_url)

    def gen_frames(self):
        global cap
        cap = cv.VideoCapture(self.url)
        
        while True:
            success, image = cap.read()
            frame_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
            frame_gray = cv.equalizeHist(frame_gray)

            ret, jpeg = cv.imencode('.jpg', image)

            frame = jpeg.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

