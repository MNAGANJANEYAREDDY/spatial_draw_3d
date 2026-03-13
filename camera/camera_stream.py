import cv2
from config import CameraConfig


class CameraStream:
    """
    Robust camera manager for Spatial Studio.

    Features
    - automatic camera detection
    - supports laptop webcam / USB / DroidCam
    - stable initialization
    """

    def __init__(self, camera_index=None):

        self.cap = None
        self.camera_index = camera_index

        self._initialize_camera()

    # ------------------------------------------------
    # Initialize Camera
    # ------------------------------------------------

    def _initialize_camera(self):

        # If user provided camera index
        if self.camera_index is not None:

            cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)

            if cap.isOpened():
                self.cap = cap
                print(f"[Camera] Using index {self.camera_index}")
                self._configure_camera()
                return

            cap.release()

        # Auto-detect camera
        for i in range(5):

            cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)

            if cap.isOpened():

                self.cap = cap
                self.camera_index = i

                print(f"[Camera] Auto-detected camera index {i}")

                self._configure_camera()
                return

            cap.release()

        raise RuntimeError("Unable to access any webcam.")

    # ------------------------------------------------
    # Configure Camera
    # ------------------------------------------------

    def _configure_camera(self):

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CameraConfig.WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CameraConfig.HEIGHT)
        self.cap.set(cv2.CAP_PROP_FPS, CameraConfig.FPS)

    # ------------------------------------------------
    # Read Frame
    # ------------------------------------------------

    def read(self):

        if self.cap is None:
            raise RuntimeError("Camera not initialized.")

        ret, frame = self.cap.read()

        if not ret:
            return None

        # mirror frame for natural interaction
        frame = cv2.flip(frame, 1)

        return frame

    # ------------------------------------------------
    # Release Camera
    # ------------------------------------------------

    def release(self):

        if self.cap is not None:
            self.cap.release()
            self.cap = None

    # ------------------------------------------------
    # Context Manager
    # ------------------------------------------------

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()