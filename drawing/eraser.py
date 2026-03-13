import math
from dataclasses import replace


class EraserEngine:

    def __init__(self, radius=60):
        self.radius = radius

    def distance(self, p1, p2):

        return math.sqrt(
            (p1[0]-p2[0])**2 +
            (p1[1]-p2[1])**2
        )

    def erase(self, strokes, point):

        new_strokes = []

        for stroke in strokes:

            kept = []

            for p in stroke.points:

                if self.distance(p, point) > self.radius:
                    kept.append(p)

                else:

                    if len(kept) > 1:
                        new_strokes.append(
                            replace(stroke, points=list(kept))
                        )

                    kept = []

            if len(kept) > 1:
                new_strokes.append(
                    replace(stroke, points=list(kept))
                )

        return new_strokes