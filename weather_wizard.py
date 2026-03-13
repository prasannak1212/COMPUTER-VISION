"""
Camera → Frame → Hand Detection → Finger Counting → Weather Effect → Display

Example Hand Landmarks
0  wrist
4  thumb tip
8  index tip
12 middle tip
16 ring tip
20 pinky tip

Final Architecture:-
Video Capture
      ↓
Frame Processing
      ↓
AI Detection (MediaPipe)
      ↓
Feature Extraction (Finger Count)
      ↓
Graphics Rendering
      ↓
Display

"""



# Used forcamera access, drawing shapes, image processing, displaying frames
import cv2 

 # Google's realtime ML framework; used for hand detection, hand landmark detection
import mediapipe as mp

# Used for mage arrays, matrix operations; Images in openCV are numpy arrays
import numpy as np

# Generating random values
import random

# Opens webcam; Internally it this creates video stream object
cap = cv2.VideoCapture(0)

# Initialize hand detectors; Mediaipipe uses ML to detect hand location and 21 hand landmarks
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Drawing utility; Mediapipe provides helper functions to draw hand skeleton, landmark points and connections
mp_draw = mp.solutions.drawing_utils

# Rain storage, a list of coordinates for rain drops
rain = []

# Infinite loop  for real time processing; This runs continously to process video frames
while True:

    # Reads camera frame and returns success boolean and image array
    ret, frame = cap.read()

    # Mirror the image; Flips image horizontally to counter mirror effect
    frame = cv2.flip(frame,1)

    # Converts color space
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Run hand detection; Mediapipe process the image and returns landmarks
    result = hands.process(rgb)

    # Finger counter
    fingers = 0

    # Check if hand is detected
    if result.multi_hand_landmarks:

        # Loop through hands; handLms contain 21 landmark points
        for handLms in result.multi_hand_landmarks:

            # Draw hand skeleton
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

            # Get landmark list; Each item of this list is a landmark and it contains x,y,z coordinates
            landmarks = handLms.landmark

            # Finger detection logic; landmarks[8] index finger tip, landmarks[6] finger joint; Because top of the screen amller 'y' value
            if landmarks[8].y < landmarks[6].y:
                fingers += 1
            if landmarks[12].y < landmarks[10].y:
                fingers += 1
            if landmarks[16].y < landmarks[14].y:
                fingers += 1
            if landmarks[20].y < landmarks[18].y:
                fingers += 1

    # Get frame size
    h,w,_ = frame.shape

    # Rain effect
    if fingers == 1:

        # Create new rain drops
        for i in range(5):
            rain.append([random.randint(0,w),0])

        # Move rain drops
        for drop in rain:

            # Increase y coordinate
            drop[1] += 10

            # Draws vertical rain line
            cv2.line(frame,(drop[0],drop[1]),(drop[0],drop[1]+10),(255,0,0),2)

        # Remove off-screen rain drops
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

    # Show frame
    cv2.imshow("Weather Wizard",frame)

    # Exit key; 27=Esc key
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Release the camera
cap.release()
cv2.destroyAllWindows()