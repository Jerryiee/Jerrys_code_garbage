import cv2
import numpy as np

# just defined variables
x1, y1, x2, y2 = 0, 0, 0, 0

#define the cerain area for cropping
area = 100

# function to set the cropping range
def set_crop(event, x, y, flags, param):
    global x1, y1, x2, y2
    if event == cv2.EVENT_RBUTTONDBLCLK:
        x1, y1, x2, y2 = x - area, y - area, x + area, y + area
        if x1 < 0:
            x1 = 0
        if y1 < 0:
            y1 = 0
        if x2 > frame.shape[1]:
            x2 = frame.shape[1]
        if y2 > frame.shape[0]:
            y2 = frame.shape[0]

# capture video
cap = cv2.VideoCapture(0)
cv2.namedWindow("Original")
cv2.setMouseCallback("Original", set_crop)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # threshold to binary image
    _, binary = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)

    # check if cropping range is set
    if x1 == 0 and y1 == 0 and x2 == 0 and y2 == 0:
        x1, y1, x2, y2 = 0, 0, frame.shape[1], frame.shape[0]

    # crop the binary image
    binary_cropped = binary[y1:y2, x1:x2]

    # find contours in the cropped binary image
    contours, _ = cv2.findContours(binary_cropped, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # find the largest contour
    if len(contours) > 0:
        largest_contour = max(contours, key=cv2.contourArea)

        # draw a bounding box around the largest contour in the cropped binary image
        x, y, w, h = cv2.boundingRect(largest_contour)
        cv2.rectangle(frame, (x1+x, y1+y), (x1+x+w, y1+y+h), (0, 255, 0), 2)

    # draw a bounding box around the cropped area in the original frame
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)



    # show the original video
    cv2.imshow("Original", frame)
    cv2.imshow("Binary", binary)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
