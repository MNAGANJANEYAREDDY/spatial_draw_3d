import cv2
import numpy as np
import math

from camera.camera_stream import CameraStream
from tracking.hand_tracker import HandTracker
from tracking.gesture_detector import GestureDetector


class SpatialStudioApp:

    def __init__(self):

        self.camera = CameraStream()
        self.tracker = HandTracker()
        self.gesture = GestureDetector()

        self.canvas = None

        self.drawing = False
        self.prev_point = None

        self.brush_size = 8
        self.eraser_size = 60

        self.objects = []

        self.current_x = 0
        self.current_y = 0

        self.angle = 0
        self.rotate = True


    # ------------------ SOLID COLORED CUBE ------------------

    def draw_tesseract(self, frame, x, y):

        size = 70

        if self.rotate:
            self.angle += 0.04

        cube = np.array([
            [-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1],
            [-1,-1,1],[1,-1,1],[1,1,1],[-1,1,1]
        ]) * size

        rot_y = np.array([
            [math.cos(self.angle),0,math.sin(self.angle)],
            [0,1,0],
            [-math.sin(self.angle),0,math.cos(self.angle)]
        ])

        cube = cube @ rot_y

        pts=[]
        for p in cube:
            pts.append((int(p[0]+x),int(p[1]+y)))

        faces=[
            [0,1,2,3],
            [4,5,6,7],
            [0,1,5,4],
            [2,3,7,6],
            [1,2,6,5],
            [0,3,7,4]
        ]

        colors=[
            (255,100,100),
            (100,255,100),
            (100,100,255),
            (255,255,100),
            (255,100,255),
            (100,255,255)
        ]

        for f,c in zip(faces,colors):

            poly=np.array([
                pts[f[0]],
                pts[f[1]],
                pts[f[2]],
                pts[f[3]]
            ])

            cv2.fillConvexPoly(frame,poly,c)
            cv2.polylines(frame,[poly],True,(0,0,0),2)


    # ------------------ SOLID SEGMENTED SPHERE ------------------

    def draw_earth(self, frame, x, y):

        r = 75

        if self.rotate:
            self.angle += 0.03

        cv2.circle(frame,(x,y),r,(200,150,40),-1)

        colors=[
            (255,120,120),
            (120,255,120),
            (120,120,255),
            (255,255,120)
        ]

        for i,c in enumerate(colors):

            ry=int(r*math.cos(math.radians(-60+i*40)))

            cv2.ellipse(
                frame,
                (x,y),
                (r,abs(ry)),
                0,
                0,
                360,
                c,
                3
            )

        for lon in range(0,360,30):

            rad=math.radians(lon+self.angle*60)

            x1=int(x+r*math.cos(rad))
            y1=int(y+r*math.sin(rad))

            x2=int(x-r*math.cos(rad))
            y2=int(y-r*math.sin(rad))

            cv2.line(frame,(x1,y1),(x2,y2),(255,255,255),1)


    # ------------------ PYRAMID ------------------

    def draw_pyramid(self, frame, x, y):

        size=70

        if self.rotate:
            self.angle+=0.05

        rot=int(30*math.sin(self.angle))

        base=[
            (x-size+rot,y+size),
            (x+size+rot,y+size),
            (x+size-rot,y-size),
            (x-size-rot,y-size)
        ]

        top=(x,y-120)

        for i in range(4):
            cv2.line(frame,base[i],base[(i+1)%4],(0,255,255),2)

        for p in base:
            cv2.line(frame,p,top,(0,255,255),2)


    # ------------------ MAIN LOOP ------------------

    def run(self):

        while True:

            frame=self.camera.read()

            if frame is None:
                break

            if self.canvas is None:
                self.canvas=frame.copy()*0

            hands,frame=self.tracker.process(frame)

            if hands:

                for hand in hands:

                    label=hand["label"]
                    gestures=self.gesture.interpret(hand)

                    x,y=hand["pixel_landmarks"][8]

                    self.current_x=x
                    self.current_y=y

                    if label=="Right":

                        if gestures["draw"] and not gestures["stop"]:

                            if not self.drawing:
                                self.prev_point=(x,y)
                                self.drawing=True

                            cv2.line(
                                self.canvas,
                                self.prev_point,
                                (x,y),
                                (0,255,255),
                                self.brush_size
                            )

                            self.prev_point=(x,y)

                        else:
                            self.drawing=False
                            self.prev_point=None


                    if label=="Left":

                        if gestures["erase"]:

                            cv2.circle(
                                self.canvas,
                                (x,y),
                                self.eraser_size,
                                (0,0,0),
                                -1
                            )

                            cv2.circle(
                                frame,
                                (x,y),
                                self.eraser_size,
                                (0,0,255),
                                2)


            for obj in self.objects:

                shape,ox,oy=obj

                if self.rotate:
                    ox=self.current_x
                    oy=self.current_y

                if shape=="cube":
                    self.draw_tesseract(frame,ox,oy)

                elif shape=="sphere":
                    self.draw_earth(frame,ox,oy)

                elif shape=="pyramid":
                    self.draw_pyramid(frame,ox,oy)


            gray=cv2.cvtColor(self.canvas,cv2.COLOR_BGR2GRAY)
            _,mask=cv2.threshold(gray,1,255,cv2.THRESH_BINARY)

            mask_inv=cv2.bitwise_not(mask)

            frame_bg=cv2.bitwise_and(frame,frame,mask=mask_inv)
            canvas_fg=cv2.bitwise_and(self.canvas,self.canvas,mask=mask)

            frame=cv2.add(frame_bg,canvas_fg)


            cv2.imshow("Spatial Studio",frame)

            key=cv2.waitKey(1)

            if key==27:
                break

            elif key==ord('1'):
                self.objects.append(("cube",self.current_x,self.current_y))

            elif key==ord('2'):
                self.objects.append(("sphere",self.current_x,self.current_y))

            elif key==ord('3'):
                self.objects.append(("pyramid",self.current_x,self.current_y))

            elif key==ord('0'):
                self.rotate=False

            elif key==ord('s'):
                cv2.imwrite("spatial_capture.png",frame)
                print("Saved screenshot")

        self.camera.release()
        cv2.destroyAllWindows()


if __name__=="__main__":

    app=SpatialStudioApp()
    app.run()