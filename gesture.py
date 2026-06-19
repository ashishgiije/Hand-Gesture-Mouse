import cv2
import mediapipe as mp
import pyautogui
import numpy as np

# Initialize MediaPipe Hand Tracking
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)

# Get screen size
screen_width, screen_height = pyautogui.size()

# Initialize variables
prev_x, prev_y = 0, 0
dragging = False

# OpenCV Video Capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Flip horizontally
    h, w, _ = frame.shape

    # Convert to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process frame with MediaPipe
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get landmark positions
            landmarks = hand_landmarks.landmark
            index_finger = landmarks[8]  # Index Finger Tip
            thumb = landmarks[4]  # Thumb Tip

            # Convert to screen coordinates
            index_x, index_y = int(index_finger.x * w), int(index_finger.y * h)
            screen_x, screen_y = int(index_finger.x * screen_width), int(index_finger.y * screen_height)

            # Move the mouse smoothly
            pyautogui.moveTo(screen_x, screen_y, duration=0.1)

            # Calculate distance between thumb and index finger
            thumb_x, thumb_y = int(thumb.x * w), int(thumb.y * h)
            distance = np.linalg.norm(np.array([index_x, index_y]) - np.array([thumb_x, thumb_y]))
           # print ("dist=",distance)
            # If fingers are close together, start dragging
            if distance < 100:
                if not dragging:
                    pyautogui.mouseDown()
                    dragging = True
            else:
                if dragging:
                    pyautogui.mouseUp()
                    dragging = False

    # Display output
    cv2.imshow("Hand Gesture Mouse (Drag & Drop)", frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
