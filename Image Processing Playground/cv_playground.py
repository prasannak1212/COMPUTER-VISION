import cv2

# Load image
image = cv2.imread("image.png")

# Resize for easier display
image = cv2.resize(image, (800,600))

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Window
cv2.namedWindow("Playground")

# Create trackbars
cv2.createTrackbar("Blur","Playground",1,50,lambda x:None)
cv2.createTrackbar("Threshold","Playground",127,255,lambda x:None)
cv2.createTrackbar("Canny1","Playground",50,255,lambda x:None)
cv2.createTrackbar("Canny2","Playground",150,255,lambda x:None)

while True:

    # Trackbar values
    blur_val = cv2.getTrackbarPos("Blur","Playground")
    thresh_val = cv2.getTrackbarPos("Threshold","Playground")
    canny1 = cv2.getTrackbarPos("Canny1","Playground")
    canny2 = cv2.getTrackbarPos("Canny2","Playground")

    # Blur must be odd
    if blur_val % 2 == 0:
        blur_val += 1
    if blur_val < 1:
        blur_val = 1

    # Apply blur
    blur = cv2.GaussianBlur(gray,(blur_val,blur_val),0)

    # Threshold
    _,thresh = cv2.threshold(blur,thresh_val,255,cv2.THRESH_BINARY)

    # Canny edges
    edges = cv2.Canny(blur,canny1,canny2)

    # Stack results
    combined = cv2.hconcat([gray,blur])
    combined2 = cv2.hconcat([thresh,edges])
    final = cv2.vconcat([combined,combined2])

    cv2.imshow("Playground",final)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()