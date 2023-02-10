import cv2
import mediapipe as mp
import time
from handDetectingModule import handDetector


cap = cv2.VideoCapture(0)

pTime = 0
cTime = 0
detector = handDetector()

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    detector.findPosition(img)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    flipimg = cv2.flip(img,1)
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)
    cv2.imshow("Image", flipimg)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break
cap.release()

    

    