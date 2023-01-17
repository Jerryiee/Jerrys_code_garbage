import cv2

# Load the cascade for face detection
face_cascade = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_default.xml")

# Capture video from the webcam
cap = cv2.VideoCapture(0)

# Function to calculate distance from the face using the width of the rectangle
def calculate_distance(width, focal_length, known_width):
    return (focal_length * known_width) / width

while True:
    # Read a frame from the webcam
    _, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Iterate over the detected faces
    for (x, y, w, h) in faces:
        # Draw a rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Calculate the distance from the face using the width of the rectangle
        focal_length = 80
        known_width = 150 # mm
        distance = calculate_distance(w, focal_length, known_width)
        distance1 = round(distance, 2)

        # Put the distance on the frame
        cv2.putText(frame, f"Distance: {distance1} cm", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    # Show the frame
    cv2.imshow("Face Detection", frame)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()
