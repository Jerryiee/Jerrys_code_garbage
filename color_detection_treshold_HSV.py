import cv2
import numpy as np

# Open a video capture object
cap = cv2.VideoCapture(0)

# Create the window for the threshold sliders
cv2.namedWindow("Threshold")
# Create the sliders for the minimum and maximum HSV values
cv2.createTrackbar("Hue Min", "Threshold", 0, 180, lambda x:x)
cv2.createTrackbar("Hue Max", "Threshold", 180, 180, lambda x:x)
cv2.createTrackbar("Sat Min", "Threshold", 0, 255, lambda x:x)
cv2.createTrackbar("Sat Max", "Threshold", 255, 255, lambda x:x)
cv2.createTrackbar("Val Min", "Threshold", 0, 255, lambda x:x)
cv2.createTrackbar("Val Max", "Threshold", 255, 255, lambda x:x)

# define the range for hsv values
range_h = 10
range_s = 50
range_v = 50

# Define a callback function to get the mouse click position
def on_mouse(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Get the HSV color of the clicked point
        hsv_clicked = cv2.cvtColor(np.uint8([[frame[y, x]]]), cv2.COLOR_BGR2HSV)[0][0]

        # Set the slider values to a range around the clicked point's HSV values
        cv2.setTrackbarPos("Hue Min", "Threshold", max(0, hsv_clicked[0] - range_h))
        cv2.setTrackbarPos("Hue Max", "Threshold", min(180, hsv_clicked[0] + range_h))
        cv2.setTrackbarPos("Sat Min", "Threshold", max(0, hsv_clicked[1] - range_s))
        cv2.setTrackbarPos("Sat Max", "Threshold", min(255, hsv_clicked[1] + range_s))
        cv2.setTrackbarPos("Val Min", "Threshold", max(0, hsv_clicked[2] - range_v))
        cv2.setTrackbarPos("Val Max", "Threshold", min(255, hsv_clicked[2] + range_v))
        print("HSV Color:", hsv_clicked)

while True:
    # Read a frame
    _, frame = cap.read()

    # Get the current values of the sliders
    h_min = cv2.getTrackbarPos("Hue Min", "Threshold")
    h_max = cv2.getTrackbarPos("Hue Max", "Threshold")
    s_min = cv2.getTrackbarPos("Sat Min", "Threshold")
    s_max = cv2.getTrackbarPos("Sat Max", "Threshold")
    v_min = cv2.getTrackbarPos("Val Min", "Threshold")
    v_max = cv2.getTrackbarPos("Val Max", "Threshold")

    # Convert the frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold the image based on the current slider values
    mask = cv2.inRange(hsv, (h_min, s_min, v_min), (h_max, s_max, v_max))

    # Perform morphological operations to clean up the thresholded image
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # Find contours in the thresholded image
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw the contours on the original frame
    #cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

    # Draw a bounding box around the largest contour
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)


    # Show the thresholded image and the original frame
    cv2.imshow("Binary", mask)
    cv2.imshow("Webcam", frame)

    # Set the callback function for the window
    cv2.setMouseCallback("Webcam", on_mouse)

    # Exit if the user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object
cap.release()

# Close all windows
cv2.destroyAllWindows()
