import cv2
from threading import Thread
import time

class WebcamStream:
    """
    defining a helper class for implementing multi-threaded processing
    """
    def __init__(self, stream_id=0):
        self.stream_id = int(stream_id)  # default is 0 for primary camera
        # opening video capture stream
        self.vcap = cv2.VideoCapture(self.stream_id)
        if self.vcap.isOpened() is False:
            print("[Exiting]: Error accessing webcam stream.")
            exit(0)
        # reading a single frame from vcap stream for initializing
        self.grabbed, self.frame = self.vcap.read()
        if self.grabbed is False:
            print('[Exiting] No more frames to read')
            exit(0)
        # self.stopped is set to False when frames are being read from self.vcap stream
        self.stopped = True
        # reference to the thread for reading next available frame from input stream
        self.t = Thread(target=self.update)
        self.t.daemon = True  # daemon threads keep running in the background while the program is executing

    # method for starting the thread for grabbing next available frame in input stream
    def start(self):
        self.stopped = False
        self.t.start()

    # method for reading next frame
    def update(self):
        while True:
            if self.stopped is True:
                break
            self.grabbed, self.frame = self.vcap.read()
            if self.grabbed is False:
                print('[Exiting] No more frames to read')
                self.stopped = True
                break
        self.vcap.release()

    # method for returning latest read frame
    def read(self):
        return self.frame

    # method called to stop reading frames
    def stop(self):
        self.stopped = True

    def generate_frames(self):
        self.start()

        while True:
            if self.stopped is True:
                break
            else:
                frame = self.read()

            if frame is None:
                continue

            # encode the frame in JPEG format
            ret, jpeg = cv2.imencode('.jpg', frame)
            # ensure the frame was successfully encoded
            if not ret:
                continue

            frame = jpeg.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


class VideoCapture:
    """
    TODO: add docstring
    """
    def __init__(self, video_source=0, width=None, height=None, fps=None):
        """TODO: add docstring"""

        self.video_source = video_source
        self.width = width
        self.height = height
        self.fps = fps

        self.running = False

        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("[MyVideoCapture] Unable to open video source", video_source)

        # Get video source width and height
        if not self.width:
            self.width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))  # convert float to int
        if not self.height:
            self.height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))  # convert float to int
        if not self.fps:
            self.fps = int(self.vid.get(cv2.CAP_PROP_FPS))  # convert float to int

        # default value at start
        self.ret = False
        self.frame = None
        self.image = None

        self.convert_color = cv2.COLOR_BGR2RGB

        # start thread
        self.running = True
        self.thread = Thread(target=self.process)
        self.thread.start()

    def process(self):
        """TODO: add docstring"""

        while self.running:
            ret, frame = self.vid.read()

            if ret:
                # process image
                frame = cv2.resize(frame, (self.width, self.height))

            else:
                print('[MyVideoCapture] stream end:', self.video_source)
                # TODO: reopen stream
                self.running = False
                break

            # assign new frame
            self.ret = ret
            self.frame = frame

    def get_frame(self):
        """TODO: add docstring"""
        return self.ret, self.frame

    def __del__(self):
        """
        Release the video source when the object is destroyed
        """

        # stop thread
        if self.running:
            self.running = False
            self.thread.join()

        # relase stream
        if self.vid.isOpened():
            self.vid.release()


class CameraUp:
    def __init__(self, source=0, width=None, height=None, sources=None):
        """TODO: add docstring"""

        self.source = source
        self.width = width
        self.height = height
        self.other_sources = sources

        # self.window.title(window_title)
        self.vid = VideoCapture(self.source, self.width, self.height)

        # After it is called once, the update method will be automatically called every delay milliseconds
        # calculate delay using `FPS`
        self.delay = int(1000 / self.vid.fps)

        self.running = True
        self.update_frame()

    def start(self):
        """TODO: add docstring"""

        if not self.running:
           self.running = True
           self.update_frame()

    def stop(self):
        """TODO: add docstring"""

        if self.running:
          self.running = False

    def update_frame(self):
        """TODO: add docstring"""

        # widgets in tkinter already have method `update()` so I have to use different name -

        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            self.image = frame

        if self.running:
            self.after(self.delay, self.update_frame)

    def select_source(self):
        """TODO: add docstring"""
        self.vid = VideoCapture(self.source, self.width, self.height)


