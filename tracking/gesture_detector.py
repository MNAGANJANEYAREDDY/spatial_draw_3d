class GestureDetector:

    INDEX_TIP = 8
    INDEX_PIP = 6

    MIDDLE_TIP = 12
    MIDDLE_PIP = 10

    RING_TIP = 16
    RING_PIP = 14

    PINKY_TIP = 20
    PINKY_PIP = 18

    # -----------------------------

    def finger_up(self, hand, tip, pip):

        tip_y = hand["pixel_landmarks"][tip][1]
        pip_y = hand["pixel_landmarks"][pip][1]

        return tip_y < pip_y

    def finger_down(self, hand, tip, pip):

        tip_y = hand["pixel_landmarks"][tip][1]
        pip_y = hand["pixel_landmarks"][pip][1]

        return tip_y > pip_y

    # -----------------------------

    def detect_draw(self, hand):

        return self.finger_up(hand, self.INDEX_TIP, self.INDEX_PIP)

    def detect_stop(self, hand):

        fingers = [

            self.finger_up(hand, self.INDEX_TIP, self.INDEX_PIP),
            self.finger_up(hand, self.MIDDLE_TIP, self.MIDDLE_PIP),
            self.finger_up(hand, self.RING_TIP, self.RING_PIP),
            self.finger_up(hand, self.PINKY_TIP, self.PINKY_PIP)

        ]

        return all(fingers)

    def detect_fist(self, hand):

        fingers = [

            self.finger_down(hand, self.INDEX_TIP, self.INDEX_PIP),
            self.finger_down(hand, self.MIDDLE_TIP, self.MIDDLE_PIP),
            self.finger_down(hand, self.RING_TIP, self.RING_PIP),
            self.finger_down(hand, self.PINKY_TIP, self.PINKY_PIP)

        ]

        return all(fingers)

    # -----------------------------

    def interpret(self, hand):

        return {

            "draw": self.detect_draw(hand),
            "stop": self.detect_stop(hand),
            "erase": self.detect_fist(hand)

        }