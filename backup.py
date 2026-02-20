import cv2
import mediapipe as mp
import time
import os
from collections import deque

# ------------------ Camera ------------------
cap = cv2.VideoCapture(0)

# ---------------- MediaPipe -----------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# ---------------- Landmarks -----------------
finger_tips = [4, 8, 12, 16, 20]
finger_pips = [2, 6, 10, 14, 18]

# ---------------- Gesture logic -------------
gesture_buffer = deque(maxlen=10)
stable_gesture = "NONE"
last_action_time = 0
COOLDOWN = 1.2  # seconds

prev_time = 0

# ---------------- VLC Control ---------------
def control_vlc(gesture):
    if gesture == "OPEN_PALM":
        os.system("xdotool key space")
    elif gesture == "TWO_FINGERS":
        os.system("xdotool key ctrl+Up")
    elif gesture == "ONE_FINGER":
        os.system("xdotool key ctrl+Down")
    elif gesture == "FIST":
        os.system("xdotool key m")

def get_gesture(finger_count):
    if finger_count == 5:
        return "OPEN_PALM"
    elif finger_count == 2:
        return "TWO_FINGERS"
    elif finger_count == 1:
        return "ONE_FINGER"
    elif finger_count == 0:
        return "FIST"
    else:
        return "UNKNOWN"

# ---------------- Main Loop -----------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    finger_count = -1
    hand_label = None

    if result.multi_handedness:
        hand_label = result.multi_handedness[0].classification[0].label

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            lm = hand_landmarks.landmark
            finger_count = 0

            # Thumb (best-effort)
            if hand_label == "Right":
                if lm[4].x < lm[2].x:
                    finger_count += 1
            elif hand_label == "Left":
                if lm[4].x > lm[2].x:
                    finger_count += 1

            # Other fingers
            for i in range(1, 5):
                if lm[finger_tips[i]].y < lm[finger_pips[i]].y:
                    finger_count += 1

    # -------- Gesture Stability --------
    if finger_count != -1:
        gesture = get_gesture(finger_count)
        gesture_buffer.append(gesture)

        if gesture_buffer.count(gesture) >= 7:
            stable_gesture = gesture

    # -------- Trigger VLC Action --------
    current_time = time.time()
    if stable_gesture != "NONE" and (current_time - last_action_time) > COOLDOWN:
        control_vlc(stable_gesture)
        last_action_time = current_time
        stable_gesture = "NONE"   # reset after trigger
        gesture_buffer.clear()

    # -------- FPS --------
    curr_time = time.time()
    fps = int(1 / (curr_time - prev_time)) if prev_time else 0
    prev_time = curr_time

    # -------- Display --------
    cv2.putText(frame, f"FPS: {fps}", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Step 4 - Gesture Controlled VLC", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
