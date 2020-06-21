import time
from threading import Event, Lock, Thread

import cv2


class ConcurrentVideoCapture(Thread):
    """Runs concurrently a cv2.VideoCapture for reading images in a separate thread.
    It follows the same api as cv2, so minimal change of code is required.

    Example:
        ```python
        cap = ConcurrentVideoCapture(0)
        while True:
            grabbed, frame = cap.read()
            # Process frame...
        cap.release()
        ```
    """

    def __init__(self, src, transform_fn=None, return_rgb=False, daemon=True):
        """Initializes the VideoCapture object with same API as cv2.VideoCapture

        Args:
            src (int or str): Camera id to open for image reading. It can be
            also a string with the full path to the device i.e "/dev/video0".
            transform_fn (python function, optional): Python function that is
            applied to each frame in the thread. Defaults to None.
            return_rgb (bool, optional): Whether or not to return the frame read
            as RGB, since by default cv2 returns it as BGR. Defaults to False.
            daemon (bool, optional): Whether or not the thread is daemonic or not,
            this means that when parent process dies, this also ends. Defaults to True.
        """
        super(ConcurrentVideoCapture, self).__init__()
        self.src = src
        self.transform_fn = transform_fn
        self.return_rgb = return_rgb
        self.cap = cv2.VideoCapture(self.src)

        self.read_lock = Lock()
        self.run_event = Event()
        self.daemon = daemon

        # if is desired RGB, add to transform_fn
        if self.return_rgb:
            old_transform_fn = self.transform_fn

            def new_fn(image):
                image = (
                    old_transform_fn(image) if old_transform_fn is not None else image
                )
                image = image[..., ::-1]
                return image

            self.transform_fn = new_fn

    # ---- Expose same methods as cv2.VideoCapture ----
    def set(self, prop, value):
        self.cap.set(prop, value)

    def get(self, prop):
        self.cap.get(prop)

    def getBackendName(self):
        return self.cap.getBackendName()

    def isOpened(self):
        return self.cap.isOpened()

    def setExceptionMode(self, value):
        self.cap.setExceptionMode(value)

    def getExceptionMode(self):
        self.cap.getExceptionMode()

    # ----  ----

    def _start_capture(self):
        if self.run_event.is_set():
            print("[Warning] Video capturing has already been started.")
            return False

        self.run_event.set()
        self.start()
        return True

    def run(self):
        while self.run_event.is_set():
            grabbed, frame = self.cap.read()
            # Apply transform function if any
            frame = (
                self.transform_fn(frame)
                if frame is not None and self.transform_fn is not None
                else frame
            )

            with self.read_lock:
                self.frame = frame
                self.grabbed = grabbed
                self.new_frame = True

    def read(self):
        if not self.run_event.is_set():
            self.grabbed, self.frame = self.cap.read()
            grabbed, frame = self.grabbed, self.frame
            self._start_capture()
            self.new_frame = False

        else:
            # Wait for a new frame to be read
            while not self.new_frame:
                time.sleep(0.001)

            with self.read_lock:
                frame = self.frame.copy() if self.frame is not None else None
                grabbed = self.grabbed
                self.new_frame = False

        return grabbed, frame

    def release(self):
        self.run_event.clear()
        self.join()
        self.cap.release()

    def __exit__(self, exec_type, exc_value, traceback):
        self.cap.release()
