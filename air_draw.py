import cv2
import numpy as np

# webcam
cap = cv2.VideoCapture(0)

# drawing canvas
canvas = None

while True:

    ret, frame = cap.read()
    frame = cv2.flip(frame,1)

    if canvas is None:
        canvas = np.zeros_like(frame)

    # convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # blue color range
    lower_blue = np.array([0,0,150])
    upper_blue = np.array([50,50,255])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # find contours
    contours,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:

        cnt = max(contours, key=cv2.contourArea)

        if cv2.contourArea(cnt) > 1000:

            x,y,w,h = cv2.boundingRect(cnt)

            cx = x + w//2
            cy = y + h//2

            cv2.circle(frame,(cx,cy),10,(0,255,0),-1)

            cv2.circle(canvas,(cx,cy),5,(255,0,0),-1)

    combined = cv2.add(frame, canvas)

    cv2.imshow("Air Draw", combined)
    cv2.imshow("Mask", mask)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()