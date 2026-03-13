import cv2
import time
import numpy as np


class Renderer3D:
    """
    Spatial Studio Rendering Engine

    Handles:
    - layered rendering
    - stroke drawing
    - current stroke drawing
    - eraser rendering
    - cube overlay
    - cursor rendering
    - UI overlay
    - performance metrics
    """

    def __init__(self):

        self.prev_time = time.time()

        # layers
        self.stroke_layer = None
        self.effect_layer = None

    # --------------------------------------------------
    # Initialize render layers
    # --------------------------------------------------

    def initialize_layers(self, frame):

        h, w, _ = frame.shape

        self.stroke_layer = np.zeros((h, w, 3), dtype=np.uint8)
        self.effect_layer = np.zeros((h, w, 3), dtype=np.uint8)

    # --------------------------------------------------
    # Render completed strokes
    # --------------------------------------------------

    def render_strokes(self, strokes):

        for stroke in strokes:

            pts = stroke.points

            for i in range(1, len(pts)):

                cv2.line(
                    self.stroke_layer,
                    pts[i - 1],
                    pts[i],
                    stroke.color,
                    stroke.thickness,
                    cv2.LINE_AA
                )

    # --------------------------------------------------
    # Render current drawing stroke
    # --------------------------------------------------

    def render_current(self, frame, points, color, thickness):

        for i in range(1, len(points)):

            cv2.line(
                frame,
                points[i - 1],
                points[i],
                color,
                thickness,
                cv2.LINE_AA
            )

    # --------------------------------------------------
    # Cursor effect
    # --------------------------------------------------

    def render_cursor(self, frame, position):

        cv2.circle(frame, position, 6, (0, 255, 0), -1)

        cv2.circle(frame, position, 15, (0, 255, 0), 1)

    # --------------------------------------------------
    # Eraser visualization
    # --------------------------------------------------

    def render_eraser(self, frame, position, radius):

        overlay = frame.copy()

        cv2.circle(overlay, position, radius, (0, 0, 255), -1)

        alpha = 0.2

        cv2.addWeighted(
            overlay,
            alpha,
            frame,
            1 - alpha,
            0,
            frame
        )

        cv2.circle(frame, position, radius, (0, 0, 255), 2)

    # --------------------------------------------------
    # Cube rendering
    # --------------------------------------------------

    def render_cube(self, frame, position):

        x, y = position
        size = 40

        pts = np.array([
            [x - size, y - size],
            [x + size, y - size],
            [x + size, y + size],
            [x - size, y + size]
        ])

        cv2.polylines(frame, [pts], True, (255, 255, 0), 2)

    # --------------------------------------------------
    # Merge layers
    # --------------------------------------------------

    def compose(self, frame):

        cv2.add(frame, self.stroke_layer, frame)

    # --------------------------------------------------
    # UI overlay
    # --------------------------------------------------

    def render_ui(self, frame, slide_number):

        cv2.putText(
            frame,
            "SPATIAL STUDIO",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            "Index Finger: Draw",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            "Left Fist: Erase",
            (20, 110),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 255),
            2
        )

        cv2.putText(
            frame,
            f"Slide: {slide_number}",
            (20, 150),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 0),
            2
        )

    # --------------------------------------------------
    # FPS
    # --------------------------------------------------

    def render_fps(self, frame):

        current = time.time()

        fps = 1 / (current - self.prev_time)

        self.prev_time = current

        cv2.putText(
            frame,
            f"FPS: {int(fps)}",
            (1050, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )