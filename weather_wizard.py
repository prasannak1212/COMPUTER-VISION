"""
Camera → Frame → Hand Detection → Finger Counting → Weather Effect → Display

"""


import cv2
import mediapipe as mp
import numpy as np
import random

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

mp_draw = mp.solutions.drawing_utils

rain = []

while True:

    ret, frame = cap.read()
    frame = cv2.flip(frame,1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb)

    fingers = 0

    if result.multi_hand_landmarks:

        for handLms in result.multi_hand_landmarks:

            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

            landmarks = handLms.landmark

            if landmarks[8].y < landmarks[6].y:
                fingers += 1
            if landmarks[12].y < landmarks[10].y:
                fingers += 1
            if landmarks[16].y < landmarks[14].y:
                fingers += 1
            if landmarks[20].y < landmarks[18].y:
                fingers += 1

    h,w,_ = frame.shape

    # Rain effect
    if fingers == 1:

        for i in range(5):
            rain.append([random.randint(0,w),0])

        for drop in rain:

            drop[1] += 10
            cv2.line(frame,(drop[0],drop[1]),(drop[0],drop[1]+10),(255,0,0),2)

        rain[:] = [d for d in rain if d[1] < h]

        cv2.putText(frame,"RAIN",(50,80),cv2.FONT_HERSHEY_SIMPLEX,2,(255,0,0),3)

    # Snow effect
    elif fingers == 2:

        for i in range(5):
            x = random.randint(0,w)
            y = random.randint(0,h)
            cv2.circle(frame,(x,y),3,(255,255,255),-1)

        cv2.putText(frame,"SNOW",(50,80),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),3)

    # Lightning
    elif fingers == 3:

        cv2.putText(frame,"LIGHTNING",(50,80),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,255),3)

        for i in range(5):
            x1 = random.randint(0,w)
            x2 = x1 + random.randint(-30,30)
            cv2.line(frame,(x1,0),(x2,h),(0,255,255),2)

    else:
        cv2.putText(frame,"CLEAR",(50,80),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),3)

    cv2.imshow("Weather Wizard",frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()