import cv2
import time
import numpy as np
import handTrackModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()

volRange = volume.GetVolumeRange()
minVol = volRange[0]  # which is -65
maxVol = volRange[1]  # which is 0

##############################################
wCam, hCam = 640, 480
##############################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
vol = 0
volBar = 400  # first initialise value should be 0 which is 400 pixel
volPer = 0
detector = htm.handDetector(detectionCon=0.7)

while True:
    success, img = cap.read()
    img = detector.findHands(img)  # location of hands and accept image
    lmList = detector.findPosition(img, draw=False)  #
    if len(lmList) != 0:
        # print(lmList[4], lmList[8])
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

        length = math.hypot(x2 - x1, y2 - y1)
        # print(length)

        # hand range is 50 to 300
        # convert to volume range -65 to 0(max)
        # use numpy to equalise

        vol = np.interp(length, [50, 250], [minVol, maxVol])  # normalising volume to range
        volBar = np.interp(length, [50, 250],
                           [400, 150])  # vol for bar becasue else range to big and goes out of window
        volPer = np.interp(length, [50, 250], [0, 100]) # for volume percentage 0 - 100
        print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None)
        if length < 50:
            cv2.circle(img, (cx, cy), 10, (0, 255, 255), cv2.FILLED)

    cv2.rectangle(img, (50, int(volBar)), (80, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)}%', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
    cv2.imshow("img", img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break




















"""
################################
wCam, hCam = 640, 480
################################
 
cap = cv2.VideoCapture(1)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
 
detector = htm.handDetector(detectionCon=0.7)
 
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange&#91;0]
maxVol = volRange&#91;1]
vol = 0
volBar = 400
volPer = 0
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        # print(lmList&#91;4], lmList&#91;8])
 
        x1, y1 = lmList&#91;4]&#91;1], lmList&#91;4]&#91;2]
        x2, y2 = lmList&#91;8]&#91;1], lmList&#91;8]&#91;2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
 
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
 
        length = math.hypot(x2 - x1, y2 - y1)
        # print(length)
 
        # Hand range 50 - 300
        # Volume Range -65 - 0
 
        vol = np.interp(length, &#91;50, 300], &#91;minVol, maxVol])
        volBar = np.interp(length, &#91;50, 300], &#91;400, 150])
        volPer = np.interp(length, &#91;50, 300], &#91;0, 100])
        print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None)
 
        if length &lt; 50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
 
    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)
 
 
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
 
    cv2.imshow("Img", img)
    cv2.waitKey(1)
 
"""
