# Gesture Mapping and Control Reference

## Gesture Recognition Details

### 1. Open Palm (5 Fingers)
**Description:** All five fingers extended, palm facing camera
**VLC Action:** Play/Pause
**Keyboard Command:** `Space`
**Use Case:** Toggle between playing and paused states

**Detection Logic:**
```
if finger_count == 5:
    gesture = "OPEN_PALM"
```

---

### 2. Two Fingers
**Description:** Index and middle fingers extended, other fingers closed
**VLC Action:** Volume Up
**Keyboard Command:** `Ctrl+Up`
**Use Case:** Increase media volume

**Detection Logic:**
```
if finger_count == 2:
    gesture = "TWO_FINGERS"
```

---

### 3. One Finger (Index Finger)
**Description:** Index finger extended, all other fingers closed
**VLC Action:** Volume Down
**Keyboard Command:** `Ctrl+Down`
**Use Case:** Decrease media volume

**Detection Logic:**
```
if finger_count == 1:
    gesture = "ONE_FINGER"
```

---

### 4. Fist (0 Fingers)
**Description:** All fingers closed, hand in fist position
**VLC Action:** Mute
**Keyboard Command:** `m`
**Use Case:** Toggle mute on/off

**Detection Logic:**
```
if finger_count == 0:
    gesture = "FIST"
```

---

## Gesture Stability Filtering

### Buffer Mechanism
- **Buffer Size:** 10 frames
- **Stability Threshold:** 7 consecutive identical gestures
- **Purpose:** Prevent accidental triggers from momentary hand movements

### Workflow
```
Frame 1: OPEN_PALM → buffer = [OPEN_PALM]
Frame 2: OPEN_PALM → buffer = [OPEN_PALM, OPEN_PALM]
...
Frame 7: OPEN_PALM → buffer has 7+ OPEN_PALM → gesture DETECTED
Frame 8: Gesture locked, ready for action
Frame 9-10: Any change resets buffer
```

---

## Action Cooldown

**Cooldown Period:** 1.2 seconds (between commands)

**Purpose:** 
- Prevent multiple triggers from single gesture
- Allow user time to reset hand position
- Ensure intentional, deliberate gestures

**Timeline:**
```
T=0s:    Gesture detected → Action executed (e.g., play/pause)
T=0-1.2s: Cooldown active (no new actions)
T=1.2s+: Ready for next gesture
```

---

## Hand Awareness

The system distinguishes between left and right hands for accurate thumb detection.

### Thumb Detection Logic

**Right Hand:**
```python
if lm[4].x < lm[2].x:  # Thumb tip to the left of PIP
    finger_count += 1
```

**Left Hand:**
```python
if lm[4].x > lm[2].x:  # Thumb tip to the right of PIP
    finger_count += 1
```

### Other Fingers (Consistent)
```python
for i in [1, 2, 3, 4]:  # Index, Middle, Ring, Pinky
    if lm[finger_tips[i]].y < lm[finger_pips[i]].y:  # Tip above PIP
        finger_count += 1
```

---

## Landmark Indices Reference

### Hand Landmark Points (MediaPipe)
```
0:  Wrist
1:  Thumb CMC
2:  Thumb MCP
3:  Thumb IP
4:  Thumb Tip          ← finger_tips[0]
5:  Index Finger MCP
6:  Index Finger PIP   ← finger_pips[1]
7:  Index Finger DIP
8:  Index Finger Tip   ← finger_tips[1]
...
20: Pinky Tip          ← finger_tips[4]
```

### Finger Tips Array
```python
finger_tips = [4, 8, 12, 16, 20]
# Index:       Thumb, Index, Middle, Ring, Pinky
```

### Finger PIP Array
```python
finger_pips = [2, 6, 10, 14, 18]
# Index:       Thumb, Index, Middle, Ring, Pinky
```

---

## Customizing Gestures

### Add a New Gesture Example

**Goal:** Add a "Thumbs Up" gesture for skip forward

1. **Modify `get_gesture()` function:**
```python
def get_gesture(finger_count):
    if finger_count == 5:
        return "OPEN_PALM"
    elif finger_count == 4:
        return "THUMBS_UP"  # NEW
    elif finger_count == 2:
        return "TWO_FINGERS"
    # ... rest
```

2. **Add to `control_vlc()` function:**
```python
def control_vlc(gesture):
    if gesture == "OPEN_PALM":
        os.system("xdotool key space")
    elif gesture == "THUMBS_UP":
        os.system("xdotool key Right")  # VLC skip forward
    # ... rest
```

3. **Update README gesture table**

---

## Testing Gestures

### Quick Test Procedure

1. Run: `python3 step3_gesture_stability.py`
2. Display gesture name on screen
3. Perform gesture slowly and hold for ~1 second
4. Wait for "GESTURE DETECTED" confirmation
5. Lower hand to reset
6. Repeat for each gesture

### Debug Output
```
Fingers: 5 → OPEN_PALM
Fingers: 2 → TWO_FINGERS
Fingers: 1 → ONE_FINGER
Fingers: 0 → FIST
```

---

## VLC Keyboard Shortcuts

### Default VLC Commands Used
| Command | Action |
|---------|--------|
| `Space` | Play/Pause |
| `Ctrl+Up` | Volume Up |
| `Ctrl+Down` | Volume Down |
| `m` | Mute |

### Other Useful VLC Shortcuts
```
n        → Next media
p        → Previous media
f        → Fullscreen
t        → Show time
Right    → Forward 10s
Left     → Backward 10s
0-9      → Jump to position
```

---

## Performance Considerations

### Gesture Recognition Accuracy by Conditions

| Lighting | Background | Accuracy |
|----------|-----------|----------|
| Good (200+ lux) | Contrasting | >95% |
| Moderate (100-200 lux) | Neutral | ~90% |
| Poor (<100 lux) | Similar to hand | <70% |

### Recommendations
- Use natural or diffuse lighting
- Avoid backlighting (light behind hand)
- Wear contrasting color clothing
- Maintain 50-100cm distance from camera
- Keep steady hand movements

---

## Troubleshooting Gestures

### Gesture Not Recognized
1. Check lighting conditions
2. Verify all fingers are fully extended/closed
3. Hold gesture steady for 1+ second
4. Ensure camera can see entire hand

### False Positives
1. Reduce `min_detection_confidence` in code
2. Increase gesture buffer size
3. Increase stability threshold (>7)

### Delayed Response
1. Increase gesture buffer size
2. Lower stability threshold
3. Check system CPU usage
4. Close background applications

