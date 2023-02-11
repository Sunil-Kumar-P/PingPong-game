import cv2
import mediapipe as mp

class handDetector():
    def __init__(self):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils
        
    #To Find and draw hands
    def findHands(self, img, Leftcolor, Rightcolor, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        lcolor = Leftcolor[::-1]
        rcolor = Rightcolor[::-1]
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    for id, lm in enumerate(handLms.landmark):
                        if lm.x > 0.5:
                            self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS, 
                                               self.mpDraw.DrawingSpec(color=lcolor, thickness=2, circle_radius=2), 
                                               self.mpDraw.DrawingSpec(color=lcolor, thickness=2, circle_radius=2))
                        else:
                            self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS, 
                                               self.mpDraw.DrawingSpec(color=rcolor, thickness=2, circle_radius=2), 
                                               self.mpDraw.DrawingSpec(color=rcolor, thickness=2, circle_radius=2))

        return img
    #To To Perform Movements
    def findPosition(self, img, left_paddle=None, right_paddle=None, Leftcolor=(255, 0, 0), Rightcolor=(0, 0, 255),vel=4, draw=True):
        lcolor = Leftcolor[::-1]
        rcolor = Rightcolor[::-1]
        if self.results.multi_hand_landmarks:
            for hand in self.results.multi_hand_landmarks:
                for id, lm in enumerate(hand.landmark):
                    if lm.x > 0.5:
                        h, w, c = img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        if draw:
                            cv2.circle(img, (cx, cy), 10, lcolor, cv2.FILLED)
                        if id==9:
                            if lm.y < 0.4:
                                # print("Left player to up")
                                left_paddle.move(up=True, VEL=vel)
                            elif lm.y >0.6:
                                # print("Left player to down")  
                                left_paddle.move(up=False, VEL=vel)
                          
                    else:
                        h, w, c = img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        if draw:
                            cv2.circle(img, (cx, cy), 10, rcolor, cv2.FILLED)
                            
                        if id==9:
                            if lm.y < 0.4:
                                # print("right player to up")
                                right_paddle.move(up=True, VEL=vel)
                            elif lm.y >0.6:
                                # print("right player to down")
                                right_paddle.move(up=False, VEL=vel)
                            
            