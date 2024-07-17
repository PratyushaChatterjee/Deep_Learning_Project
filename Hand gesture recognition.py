#hand gesture recognition
import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()

    if not success:
      print("Ignoring empty camera frame.")

      continue
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

    image.flags.writeable = False
    results = hands.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()

#volume control
import cv2
import mediapipe
import numpy as np
import HandTrackingModule as ht
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

cap = cv2.VideoCapture(0 , cv2.CAP_DSHOW)
cap.set(3 , 640)
cap.set(4 , 480)
detector = ht.HandDetector()
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
'''We see that the minimum range is -65 and the maximum is 0'''
'''volume.GetVolumeRange() will give the value in the form of a tuple with the minimum value , maximum value and another parameter'''
minVol = volRange[0]
maxVol = volRange[1]
while(True):
    _ , img = cap.read()
    img = cv2.flip(img , 1)
    img = detector.findHands(img)
    idList = detector.findPosition(img , False)
    if(len(idList)!=0):
        x1 , y1 = idList[4][1] , idList[4][2]
        x2 , y2 = idList[8][1] , idList[8][2]
        x3 , y3 = (x1 + x2)//2 , (y1 + y2)//2
        cv2.circle(img , (x1 , y1) , 15 , (255  , 0 , 255) , cv2.FILLED)
        cv2.circle(img , (x2 , y2) , 15 , (255  , 0 , 255) , cv2.FILLED)    
        cv2.line(img , (x1 , y1) , (x2 , y2) , (255 , 0 , 255) , 3)
        cv2.circle(img , (x3 , y3) , 15 , (255 , 0 , 255) , cv2.FILLED)
        length = math.hypot(x2 - x1 , y2 - y1)        
        print(length)
       '''Here we see the maximum length coming to be almost 400 and the minimum length to be 15'''
        if length<=50:
            cv2.circle(img , (x3 , y3) , 15 , (0 , 255 , 0) , cv2.FILLED)    
        '''Converting length to volume range'''
        vol = np.interp(length , [50 , 400] , [minVol , maxVol])
        print(int(length) , vol)
        volume.SetMasterVolumeLevel(vol , None)
        volBar = np.interp(length , [50 , 400] , [400 , 150])
        cv2.rectangle(img , (50 , 150) , (85 , 400) , (0 , 255 , 0) , 3)
        cv2.rectangle(img , (50 , int(volBar)) , (85 , 400) , (0 , 255 , 0) , cv2.FILLED)        
        volPercent = np.interp(length , [50 , 400] , [0 , 100])
        cv2.putText(img , f'{int(volPercent)} %' , (40 , 100) , cv2.FONT_HERSHEY_SCRIPT_COMPLEX , 1 , (255 , 0 , 0) , 3)
        
    cv2.imshow("Result" , img)
    cv2.waitKey(1)


#finger counting
import cv2
import numpy as np
import HandTrackingModule as ht
cap = cv2.VideoCapture(0 , cv2.CAP_DSHOW)
cap.set(3 , 700)
cap.set(4 , 600)
detector  = ht.HandDetector()
def getNumber(fingers):
    s = ""
    for i in fingers:
        s += str(i)    
    if(s == "00000"):
        return "A"
    elif(s == "10001"):
        return "Y" 
    elif(s == "00001"):
        return "I" 
    elif(s == "11000"):
        return "L"
    elif(s == "01000"):
        return 1
    elif(s == "01100"):
        return 2
    elif(s == "11100"):
        return 3
    elif(s == "01111"):
        return 4
    elif(s == "11111"):
        return 5
    elif(s == "01110"):
        return 6
    elif(s == "01101"):
        return 7
    elif(s == "01011"):
        return 8
    elif(s == "00111"):
        return 9    
while(True):
    _ , img = cap.read()    
    img = cv2.flip(img , 1)
    img = detector.findHands(img)
    idList = detector.findPosition(img , False)
    tipId = [4 , 8 , 12 , 16 , 20]
    if(len(idList)!=0):
        fingers = []
        if(idList[tipId[0]][1] < idList[tipId[0]-2][1]):
            fingers.append(1)
        else:
            fingers.append(0)        
        for id in range(1 , len(tipId)):
            if(idList[tipId[id]][2] < idList[tipId[id]-2][2]):
                fingers.append(1)
            else:
                fingers.append(0) 
        cv2.putText(img , str(getNumber(fingers)) , (45 , 375) , cv2.FONT_HERSHEY_PLAIN , 10 , (255 , 0 , 255) , 20)    
    cv2.imshow("Result" , img)
    cv2.waitKey(1)


#sign language
import cv2
import numpy as np
import HandTrackingModule as ht
cap = cv2.VideoCapture(0 , cv2.CAP_DSHOW)
cap.set(3 , 800)
cap.set(4 , 700)
detector  = ht.HandDetector()
def getNumber(fingers):
    s = ""
    for i in fingers:
        s += str(i) 
    if(s == "00011"):
        return "OKAY"
    elif(s == "01000"):
        return "OUT"
    elif(s == "01100"):
        return "VICTORY"
    elif(s== "10000"):
        return "FINE"
    elif(s== "11111"):
        return "STOP"
    elif(s== "01001"):
        return "ROCK"        
while(True):
    _ , img = cap.read()    
    img = cv2.flip(img , 1)    
    img = detector.findHands(img)
    idList = detector.findPosition(img , False)
    tipId = [4 , 8 , 12 , 16 , 20]
    if(len(idList)!=0):
        fingers = []
        if(idList[tipId[0]][1] < idList[tipId[0]-2][1]):
            fingers.append(1)
        else:
            fingers.append(0)        
        for id in range(1 , len(tipId)):
            if(idList[tipId[id]][2] < idList[tipId[id]-2][2]):
                fingers.append(1)
            else:
                fingers.append(0) 
        cv2.putText(img , str(getNumber(fingers)) , (45 , 375) , cv2.FONT_HERSHEY_PLAIN , 10 , (255 , 0 , 255) , 20)
    cv2.imshow("Result" , img)
    cv2.waitKey(1)

