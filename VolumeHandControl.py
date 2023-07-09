import HandTracking_Module as htm
import cv2
import numpy as np
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

volume = interface.QueryInterface(IAudioEndpointVolume)

# volume range is (-65.25, 0.0)
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

WCap = 640
HCap = 480
cap = cv2.VideoCapture(0)
cap.set(3, WCap)
cap.set(4, HCap)

detector = htm.HandTracking(min_detection_confidence=0.8)

curentVol = volume.GetMasterVolumeLevel()
volRect = volRect = np.interp(curentVol, [volRange[0],  volRange[1]], [200, 50])
volPer = np.interp(curentVol, [volRange[0],  volRange[1]], [0, 100]) 

while cap.isOpened():
    ret, frame = cap.read()
    frame = detector.findHands(frame)
    lmList, side = detector.findPosition(frame, draw=False)

    if len(lmList) > 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2)//2, (y1 + y2)//2

        cv2.circle(frame, (x1, y1), 5, (0, 255, 0), 2)
        cv2.circle(frame, (x2, y2), 5, (0, 255, 0), 2)
        cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.circle(frame, (cx, cy), 5, (0, 255, 0), 2, cv2.FILLED)

        ## Euclidean distance between points
        distance = math.hypot((x2 - x1), (y2 - y1))

        ## Print distance anf find min and max value, in this example min <= 10 and max = 172 so distance_rane = (10, 130)
        # print(distance)

        newVol = np.interp(distance, [10, 130], [minVol, maxVol])
        volume.SetMasterVolumeLevel(newVol, None)

        volRect = np.interp(distance, [10, 130], [200, 50])
        volPer = np.interp(distance, [10, 130], [0, 100])

    cv2.rectangle(frame, (25, 50), (55, 200), (0, 255, 0), 2)
    cv2.rectangle(frame, (25, int(volRect)), (55, 200), (255, 0, 0), cv2.FILLED)
    cv2.putText(frame, f'{int(volPer)} %', (20, 250), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow('image', frame)
    
    if cv2.waitKey(10) & 0xFF==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()