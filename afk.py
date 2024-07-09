import cv2
import mediapipe as mp

from pynput.keyboard import Controller

# Initialize MediaPipe Hands and Keyboard Controller
mp_hands = mp.solutions.hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
keyboard = Controller()

# Open the webcam
cp = cv2.VideoCapture(0)

# Initialize variables for hand landmarks
x1, x2, y1, y2 = 0, 0, 0, 0
x3, y3, x4, y4 = 0, 0, 0, 0  # Added variables for additional hand landmarks which is used for nitro

while True:
    # Read a frame from the webcam
    _, image = cp.read()

    # Flip the image horizontally for a mirror effect
    image = cv2.flip(image, 1)

    # Convert the image to RGB format
    rgb_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image to detect hands
    output_hands = mp_hands.process(rgb_img)
    all_hands = output_hands.multi_hand_landmarks

    if all_hands:
        # Get the first detected hand
        hand = all_hands[0]
        one_hand_landmark = hand.landmark

        # Iterate over each landmark of the hand
        for id, lm in enumerate(one_hand_landmark):
            # Normalization of landmarks according to the screen size
            x = int(lm.x * image.shape[1])
            y = int(lm.y * image.shape[0])

            # Assign specific landmarks to variables - Refer to mediapipe documentation
            if id == 3: # 3 is the landmark id for the ip of the thumb
                x3, y3 = x, y
            if id == 5: # 5 is the landmark id for the bottom of the index finger
                x4, y4 = x, y
            if id == 12: # 12 is the landmark id for the tip of the middle finger
                x1, y1 = x, y
            if id == 0: # 0 is the landmark id for the Wrist
                x2, y2 = x, y

        # Calculate distances between landmarks
        distX = x1 - x2
        distY = y1 - y2
        distNx = x3 - x4 # Calculate distance between additional landmarks which is used for nitro
        distNy = y3 - y4
        
        # Hand gesture controls
        # Backward
        if distY > -140 and distY != 0:
            keyboard.release('d')
            keyboard.release('a')
            keyboard.release('w')
            keyboard.press('s')
            print("S")

        # Nitro(optional)
        if distNx > -27 and abs(distNy) < 30:
            keyboard.release('s')
            keyboard.release('a')
            # keyboard.release('w')
            keyboard.release('d')
            keyboard.press('n')
            print("N") 

        # Forward
        if distY < -200 and distY != 0:
            keyboard.release('s')
            keyboard.release('n')
            keyboard.release('d')
            keyboard.release('a')
            keyboard.press('w')
            print("W")

        # Left
        if distX < -100 and distX != 0:
            keyboard.release('s')
            keyboard.release('d')
            keyboard.release('n')
            keyboard.press('w')
            keyboard.press('a')
            print('A')

        # Right
        if distX > 55 and distX != 0:
            keyboard.release('a')
            keyboard.release('s')
            keyboard.release('n')
            keyboard.press('w')
            keyboard.press('d')
            print('D')

    else:
        print('None')
        keyboard.release('d')
        keyboard.release('a')
        keyboard.release('w')
        keyboard.release('s')
        keyboard.release('n')
    cv2.imshow("Frame", image)
    
    # Wait for 'z' key to exit the loop
    z = cv2.waitKey(1)
    if z == ord("z"):
        break

# Release the webcam and close OpenCV windows
cp.release()
cv2.destroyAllWindows()
