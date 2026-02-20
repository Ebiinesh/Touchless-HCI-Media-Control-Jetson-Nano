import cv2
import mediapipe as mp
import time

# Camera
cap = cv2.VideoCapture(0)

# MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# Landmark indices
finger_tips = [4, 8, 12, 16, 20]
finger_pips = [2, 6, 10, 14, 18]

prev_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    finger_count = 0
    hand_label = None

    # Get handedness (Left / Right)
    if result.multi_handedness:
        hand_label = result.multi_handedness[0].classification[0].label

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            lm = hand_landmarks.landmark

            # ---- THUMB (hand-aware logic) ----
            if hand_label == "Right":
                if lm[finger_tips[0]].x < lm[finger_pips[0]].x:
                    finger_count += 1
            elif hand_label == "Left":
                if lm[finger_tips[0]].x > lm[finger_pips[0]].x:
                    finger_count += 1

            # ---- OTHER 4 FINGERS (vertical logic) ----
            for i in range(1, 5):
                if lm[finger_tips[i]].y < lm[finger_pips[i]].y:
                    finger_count += 1

    # FPS calculation
    curr_time = time.time()
    fps = int(1 / (curr_time - prev_time)) if prev_time else 0
    prev_time = curr_time

    # Display info
    cv2.putText(frame, f"Fingers: {finger_count}", (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    if hand_label:
        cv2.putText(frame, f"Hand: {hand_label}", (10, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    cv2.putText(frame, f"FPS: {fps}", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Step 2 - Finger Count (Fixed Thumb)", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()

