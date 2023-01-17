import cv2
import numpy as np

# Create a window with sliders for RGB min and max and brightness
cv2.namedWindow("Adjustment")
cv2.createTrackbar("R Min", "Adjustment", 0, 255, lambda x: x)
cv2.createTrackbar("G Min", "Adjustment", 0, 255, lambda x: x)
cv2.createTrackbar("B Min", "Adjustment", 0, 255, lambda x: x)
cv2.createTrackbar("R Max", "Adjustment", 255, 255, lambda x: x)
cv2.createTrackbar("G Max", "Adjustment", 255, 255, lambda x: x)
cv2.createTrackbar("B Max", "Adjustment", 255, 255, lambda x: x)
cv2.createTrackbar("Brightness", "Adjustment", 100, 200, lambda x: x)

# Create a video capture object
cap = cv2.VideoCapture(0)

def get_rgb(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        b, g, r = frame[y, x]
        deviation = 15
        lower = np.array([max(r - deviation, 0), max(g - deviation, 0), max(b - deviation, 0)])
        upper = np.array([min(r + deviation, 255), min(g + deviation, 255), min(b + deviation, 255)])
        cv2.setTrackbarPos("R Min", "Adjustment", lower[0])
        cv2.setTrackbarPos("G Min", "Adjustment", lower[1])
        cv2.setTrackbarPos("B Min", "Adjustment", lower[2])
        cv2.setTrackbarPos("R Max", "Adjustment", upper[0])
        cv2.setTrackbarPos("G Max", "Adjustment", upper[1])
        cv2.setTrackbarPos("B Max", "Adjustment", upper[2])
        print("RGB values at clicked point: ", r, g, b)
        hsv_value= np.uint8([[[b ,g, r]]])
        hsv = cv2.cvtColor(hsv_value,cv2.COLOR_BGR2HSV)
        print ("HSV : " ,hsv)
        text = "RGB: ({}, {}, {})".format(r, g, b)
        cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

while True:
    # Read the frame from the camera
    ret, frame = cap.read()
    if not ret:
        break
    cv2.namedWindow("Original")
    cv2.setMouseCallback("Original", get_rgb)
    
    # Get the current positions of the sliders
    r_min = cv2.getTrackbarPos("R Min", "Adjustment")
    g_min = cv2.getTrackbarPos("G Min", "Adjustment")
    b_min = cv2.getTrackbarPos("B Min", "Adjustment")
    r_max = cv2.getTrackbarPos("R Max", "Adjustment")
    g_max = cv2.getTrackbarPos("G Max", "Adjustment")
    b_max = cv2.getTrackbarPos("B Max", "Adjustment")
    brightness = cv2.getTrackbarPos("Brightness", "Adjustment")

    # Apply brightness to the frame
    frame = cv2.addWeighted(frame, 1, frame, 0, brightness-100)

    # Convert the frame to HSV color space
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Create a mask for the desired color range
    lower_color = np.array([r_min, g_min, b_min])
    upper_color = np.array([r_max, g_max, b_max])
    mask = cv2.inRange(rgb, lower_color, upper_color)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Draw a bounding box around the largest contour
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Show the original video, binary video, and bounding box
    cv2.imshow("Original", frame)
    cv2.imshow("Binary", mask)

    # Exit the program when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the windows
cap.release()
cv2.destroyAllWindows()