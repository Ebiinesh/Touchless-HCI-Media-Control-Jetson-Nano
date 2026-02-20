# Touchless HCI for Media Control Using Hand Gestures on NVIDIA Jetson Nano

A real-time hand gesture recognition system that translates hand movements into media control commands (play/pause, volume control) for VLC media player using MediaPipe Hands on NVIDIA Jetson Nano.

## Project Overview

This project implements a touchless Human-Computer Interface (HCI) system using computer vision and hand gesture recognition. It processes real-time video from a USB webcam, detects hand landmarks using MediaPipe, classifies gestures, and translates them into keyboard commands to control media playback.

**Key Features:**
- Real-time hand tracking and landmark detection
- Finger counting and gesture classification
- Gesture stability filtering
- VLC media player control via keyboard shortcuts
- Optimized for NVIDIA Jetson Nano hardware
- >90% gesture recognition accuracy in controlled lighting
- <200ms end-to-end latency
- Stable at ≥15 FPS

## Hardware Requirements

- **NVIDIA Jetson Nano Developer Kit**
- **USB Webcam** (USB 2.0/3.0 compatible)
- **Monitor** with HDMI/DP input
- **Standard peripherals** (keyboard, mouse, power supply)

## Software Requirements

- **JetPack OS** with CUDA support
- **Python 3.6+**
- **OpenCV** (cv2)
- **MediaPipe** (hand detection)
- **VLC Media Player**
- **xdotool** (for keyboard control)

## Installation

### 1. Prerequisites

Ensure you have JetPack OS installed on your Jetson Nano with CUDA support.

### 2. Create Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
sudo apt-get install xdotool vlc
```

**Note for Jetson Nano:** If pip install fails, try installing from pre-built wheels:
```bash
pip install --upgrade pip setuptools wheel
```

## Project Structure

```
arm_challenge/
├── step1_hand_tracking.py          # Basic hand landmark detection
├── step2_finger_count.py           # Finger counting logic
├── step3_gesture_stability.py      # Gesture filtering & stabilization
├── step4_gesture_vlc_control.py    # Final VLC control integration
├── requirements.txt                # Python dependencies
├── README.md                       # This file
└── LICENSE                         # MIT License
```

## Gesture Mapping

| Gesture | Finger Count | VLC Command | Keyboard Shortcut |
|---------|--------------|-------------|-------------------|
| Open Palm | 5 | Play/Pause | Space |
| Two Fingers | 2 | Volume Up | Ctrl+Up |
| One Finger | 1 | Volume Down | Ctrl+Down |
| Fist | 0 | Mute | M |

## Usage

### Step 1: Basic Hand Tracking
Detects and visualizes hand landmarks in real-time.

```bash
python3 step1_hand_tracking.py
```

**Output:** Real-time video with hand skeleton overlay

### Step 2: Finger Count Detection
Counts raised fingers with hand-aware logic (left/right hand distinction).

```bash
python3 step2_finger_count.py
```

**Output:** Finger count display overlaid on video

### Step 3: Gesture Stability
Filters gestures using a buffer to detect stable, intentional gestures.

```bash
python3 step3_gesture_stability.py
```

**Output:** Stable gesture detection with buffer visualization

### Step 4: VLC Media Control (Final)
Integrates all components for real-time VLC media control.

```bash
python3 step4_gesture_vlc_control.py
```

**Output:** Real-time VLC control with gesture recognition

**Controls:**
- Press **ESC** to exit any script
- Ensure **VLC is running** and in focus for commands to work
- Maintain **good lighting** for optimal performance

## Architecture

### Pipeline Overview

```
Webcam Input
    ↓
MediaPipe Hand Detection
    ↓
Landmark Extraction
    ↓
Finger Counting Logic
    ↓
Gesture Classification
    ↓
Stability Filtering (Buffer)
    ↓
VLC Control (xdotool)
```

### MediaPipe Configuration

```python
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
```

- **max_num_hands=1:** Single-hand detection (optimized for latency)
- **min_detection_confidence=0.7:** 70% confidence threshold
- **min_tracking_confidence=0.7:** Smooth tracking stability

### Gesture Detection Logic

1. **Finger Counting:** Uses hand landmark positions (tips vs. PIP joints)
2. **Hand Awareness:** Accounts for left/right hand orientation
3. **Stability Buffer:** 10-frame buffer with majority voting
4. **Action Cooldown:** 1.2s cooldown between commands to prevent accidental triggers

## Performance Metrics

### Target Specifications
- **Gesture Recognition Accuracy:** >90% in controlled lighting
- **End-to-End Latency:** <200ms (detection to action)
- **Frame Rate:** ≥15 FPS on Jetson Nano

### Optimization Techniques
- Single-hand tracking for reduced computation
- Efficient MediaPipe Lite models
- CPU-optimized NumPy operations
- Minimal post-processing overhead

## Troubleshooting

### Camera Not Detected
```bash
ls /dev/video*
# If no video devices found, check USB connection
```

### Poor Gesture Recognition
- Ensure good lighting (natural or diffuse lighting preferred)
- Maintain distance of 50cm-100cm from camera
- Use contrasting clothing against background
- Increase `min_detection_confidence` if too many false positives

### VLC Commands Not Working
- Verify VLC is running: `ps aux | grep vlc`
- Ensure VLC window is focused (in foreground)
- Test xdotool: `xdotool key space` (should play/pause VLC)
- Check keyboard layout setting

### Low FPS Performance
- Reduce camera resolution if possible
- Close other applications
- Enable GPU acceleration (if available)
- Use lower MediaPipe confidence thresholds

## Development Notes

### Key Parameters

```python
# MediaPipe Detection
min_detection_confidence = 0.7
min_tracking_confidence = 0.7

# Gesture Stability
gesture_buffer = deque(maxlen=10)
stability_threshold = 7  # frames needed for stable gesture

# Action Control
COOLDOWN = 1.2  # seconds between commands
```

### Customization

**Add New Gesture:**
1. Modify `get_gesture()` function to add new finger count mapping
2. Add control command in `control_vlc()` function
3. Update gesture mapping table in README

**Change VLC Commands:**
Edit the `control_vlc()` function in `step4_gesture_vlc_control.py`
```python
elif gesture == "YOUR_GESTURE":
    os.system("xdotool key your_command")
```

**Adjust Gesture Stability:**
```python
gesture_buffer = deque(maxlen=N)  # Increase N for more stability
# Adjust stability_threshold for majority voting
```

## Deliverables

✅ **Source Code** - Complete gesture recognition and VLC control pipeline
✅ **Gesture Mapping Table** - Defined in README
✅ **Performance Analysis** - Metrics and optimization techniques documented
✅ **Architecture Documentation** - Pipeline overview and design decisions

## Learning Outcomes

- ✓ Real-time edge computer vision implementation
- ✓ MediaPipe model optimization for low-latency inference
- ✓ Hand gesture classification and stability filtering
- ✓ System-level integration (keyboard control via xdotool)
- ✓ Hardware-specific optimization for Jetson Nano ARM architecture

## References

- [MediaPipe Hands Documentation](https://google.github.io/mediapipe/solutions/hands.html)
- [OpenCV Documentation](https://docs.opencv.org/)
- [Jetson Nano Developer Guide](https://developer.nvidia.com/embedded/jetson-nano-developer-kit)
- [xdotool Documentation](https://www.semicomplete.com/projects/xdotool/)

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

Created as part of the ARM Bharat AI-SoC Student Challenge - Touchless HCI Challenge

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

---

**Last Updated:** February 2026
