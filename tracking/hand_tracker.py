import cv2
import mediapipe as mp


class HandTracker:
    """
    Advanced hand tracking engine for Spatial Studio.

    Provides:
    - normalized landmarks
    - pixel landmarks
    - hand center
    - bounding box
    - left/right label
    """

    def __init__(
        self,
        max_hands=2,
        detection_confidence=0.7,
        tracking_confidence=0.7
    ):

        self.max_hands = max_hands

        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            model_complexity=1,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )

    # --------------------------------------------------
    # Process Frame
    # --------------------------------------------------

    def process(self, frame):

        height, width, _ = frame.shape

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.hands.process(rgb)

        detected_hands = []

        if results.multi_hand_landmarks:

            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):

                # --------------------------
                # Normalized landmarks
                # --------------------------

                norm_landmarks = []
                pixel_landmarks = []

                for lm in hand_landmarks.landmark:

                    norm_landmarks.append((lm.x, lm.y))

                    px = int(lm.x * width)
                    py = int(lm.y * height)

                    pixel_landmarks.append((px, py))

                # --------------------------
                # Bounding box
                # --------------------------

                xs = [p[0] for p in pixel_landmarks]
                ys = [p[1] for p in pixel_landmarks]

                bbox = (
                    min(xs),
                    min(ys),
                    max(xs),
                    max(ys)
                )

                # --------------------------
                # Hand center
                # --------------------------

                center_x = int(sum(xs) / len(xs))
                center_y = int(sum(ys) / len(ys))

                center = (center_x, center_y)

                # --------------------------
                # Left / Right label
                # --------------------------

                label = results.multi_handedness[idx].classification[0].label

                # --------------------------
                # Draw skeleton
                # --------------------------

                self.mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )

                detected_hands.append({

                    "label": label,
                    "landmarks": norm_landmarks,
                    "pixel_landmarks": pixel_landmarks,
                    "center": center,
                    "bbox": bbox

                })

        return detected_hands, frame