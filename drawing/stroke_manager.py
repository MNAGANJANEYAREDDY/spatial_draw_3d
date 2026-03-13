from collections import deque
import numpy as np
import time
from dataclasses import dataclass


@dataclass
class Stroke:
    points: list
    timestamp: float
    color: tuple
    thickness: int


class StrokeManager:

    def __init__(self):

        self.buffer = deque(maxlen=8)

        self.current_points = []

        self.undo_stack = []

        self.color = (255, 0, 0)
        self.thickness = 5

    # ------------------------------
    # Start stroke
    # ------------------------------

    def start_stroke(self):

        self.current_points = []
        self.buffer.clear()

    # ------------------------------
    # Add point
    # ------------------------------

    def add_point(self, point):

        self.buffer.append(point)

        x = int(np.mean([p[0] for p in self.buffer]))
        y = int(np.mean([p[1] for p in self.buffer]))

        self.current_points.append((x, y))

    # ------------------------------
    # End stroke
    # ------------------------------

    def end_stroke(self):

        if len(self.current_points) < 2:
            self.current_points = []
            return

        stroke = Stroke(
            points=list(self.current_points),
            timestamp=time.time(),
            color=self.color,
            thickness=self.thickness
        )

        self.undo_stack.append(stroke)

        self.current_points = []
        self.buffer.clear()

    # ------------------------------

    def get_current_stroke(self):

        return self.current_points