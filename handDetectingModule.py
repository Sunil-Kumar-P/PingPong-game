import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils
        
    def findHands(self, img, Leftcolor, Rightcolor, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS, 
                                               self.mpDraw.DrawingSpec(color=Leftcolor, thickness=2, circle_radius=2), 
                                               self.mpDraw.DrawingSpec(color=Rightcolor, thickness=2, circle_radius=2))

        return img
    
    def findPosition(self, img, left_paddle=None, right_paddle=None, lcolor=(255, 0, 0), rcolor=(0, 0, 255),draw=True):
        if self.results.multi_hand_landmarks:
            for hand in self.results.multi_hand_landmarks:
                for id, lm in enumerate(hand.landmark):
                    if lm.x < 0.5:
                        h, w, c = img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        if draw:
                            cv2.circle(img, (cx, cy), 10, lcolor, cv2.FILLED)
                        if id==9:
                            if lm.y < 0.4:
                                print("Left player to up")
                                left_paddle.move(up=True)
                            elif lm.y >0.6:
                                print("Left player to down")  
                                left_paddle.move(up=False)
                          
                    else:
                        h, w, c = img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        if draw:
                            cv2.circle(img, (cx, cy), 10, rcolor, cv2.FILLED)
                            
                        if id==9:
                            if lm.y < 0.4:
                                print("right player to up")
                                right_paddle.move(up=True)
                            elif lm.y >0.6:
                                print("right player to down")
                                right_paddle.move(up=False)
                            
            