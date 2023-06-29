from HandTracking_Module import HandTracking

import cv2
import time

pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
detector = HandTracking()

while True:
    success, img = cap.read()
    img = detector.findHands(img, False)
    lmList = detector.findPosition(img)
    if len(lmList) != 0:
        print(lmList[4])
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)
        cv2.imshow("Image", img)
        
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()