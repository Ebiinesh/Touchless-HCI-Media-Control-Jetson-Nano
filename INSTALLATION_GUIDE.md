# Installation Guide for Jetson Nano

Complete step-by-step installation guide for setting up the Touchless HCI Gesture Control system on NVIDIA Jetson Nano.

## Prerequisites

- NVIDIA Jetson Nano Developer Kit
- USB Webcam (USB 2.0 or 3.0)
- Monitor, keyboard, and mouse
- Power supply (5V/2.5A)
- Stable internet connection for downloading packages

## Part 1: Jetson Nano OS Setup

### 1.1 Flash JetPack OS

1. Download JetPack from [NVIDIA Developer Portal](https://developer.nvidia.com/jetpack)
2. Use NVIDIA SDK Manager or Etcher to flash microSD card
3. Insert SD card into Jetson Nano
4. Power on and complete initial setup

### 1.2 Verify CUDA Support

```bash
# Check CUDA installation
nvcc --version

# Check GPU availability
nvidia-smi
```

Expected output shows NVIDIA GPU and CUDA version.

---

## Part 2: System Dependencies

### 2.1 Update System Packages

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y build-essential python3-dev python3-pip
```

### 2.2 Install MediaPipe Dependencies

```bash
# Required by MediaPipe
sudo apt install -y libopenblas-dev libblas-dev libomp-dev
sudo apt install -y liblapack-dev libatlas-base-dev

# For video processing
sudo apt install -y libfreetype6-dev libjpeg-dev zlib1g-dev
```

### 2.3 Install System Control Tools

```bash
# For keyboard control
sudo apt install -y xdotool x11-utils

# Media player
sudo apt install -y vlc
```

### 2.4 Configure GPU Memory (Optional but Recommended)

```bash
# Edit NVRM config for optimal GPU usage
sudo jetson_clocks
```

---

## Part 3: Python Environment Setup

### 3.1 Create Virtual Environment

```bash
# Navigate to project directory
cd ~/arm_challenge

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Verify activation (should show "venv" prefix)
which python
```

### 3.2 Upgrade pip and setuptools

```bash
pip install --upgrade pip setuptools wheel

# Verify versions (pip should be 20+)
pip --version
```

---

## Part 4: Install Project Dependencies

### 4.1 Install Required Packages

```bash
# Install from requirements.txt
pip install -r requirements.txt

# This installs:
# - opencv-python (for video capture and display)
# - mediapipe (for hand detection)
# - numpy (for numerical operations)
```

**Expected installation time:** 5-15 minutes (depends on internet speed)

### 4.2 Verify Installations

```bash
# Test imports
python3 -c "import cv2; print('OpenCV:', cv2.__version__)"
python3 -c "import mediapipe; print('MediaPipe:', mediapipe.__version__)"
python3 -c "import numpy; print('NumPy:', numpy.__version__)"
```

All imports should succeed without errors.

---

## Part 5: Camera Setup

### 5.1 Verify Camera Connection

```bash
# List connected USB devices
lsusb

# List video devices
ls -l /dev/video*

# Expected: /dev/video0 or similar
```

### 5.2 Test Camera Feed

```bash
# Quick camera test
python3 << 'EOF'
import cv2
cap = cv2.VideoCapture(0)
if cap.isOpened():
    ret, frame = cap.read()
    print(f"Camera detected: {frame.shape}")
    cap.release()
else:
    print("Error: Camera not found")
EOF
```

### 5.3 Troubleshooting Camera

**Camera not detected:**
```bash
# Check permissions
sudo usermod -a -G video $USER

# Reconnect camera and log out/in
logout
# (then login again)

# Alternative: Use sudo
sudo python3 step1_hand_tracking.py
```

---

## Part 6: First Run

### 6.1 Test Hand Tracking

```bash
# Activate virtual environment if not already active
source venv/bin/activate

# Run basic hand tracking test
python3 step1_hand_tracking.py
```

**Expected behavior:**
- Camera window opens
- Your hand appears with skeleton overlay
- FPS counter displays in top-left
- Press ESC to exit

**If it fails:**
```bash
# Check for errors
python3 -c "import cv2; cap = cv2.VideoCapture(0); print(cap.isOpened())"
```

### 6.2 Test Finger Counting

```bash
python3 step2_finger_count.py
```

**Expected behavior:**
- Shows finger count (0-5)
- Displays left/right hand label
- Updates in real-time as you move fingers

### 6.3 Test Gesture Stability

```bash
python3 step3_gesture_stability.py
```

**Expected behavior:**
- Detects stable gestures (OPEN_PALM, TWO_FINGERS, etc.)
- Requires ~1 second of stable gesture
- Prevents false positives from brief movements

### 6.4 Test VLC Control (Full Integration)

```bash
# Start VLC with a media file
vlc /path/to/video.mp4 &

# Run gesture control
python3 step4_gesture_vlc_control.py

# Test gestures:
# Open palm → Play/Pause
# Two fingers → Volume Up
# One finger → Volume Down
# Fist → Mute
```

---

## Part 7: Performance Optimization

### 7.1 Enable Jetson Clocks

```bash
# Set CPU/GPU to maximum frequency
sudo jetson_clocks

# Run in background (recommended for development)
sudo jetson_clocks --show
```

### 7.2 Monitor Performance

```bash
# Check CPU/GPU usage
watch -n 0.1 nvidia-smi

# Monitor thermal conditions
cat /sys/devices/virtual/thermal/cooling_device*/type
```

### 7.3 Reduce System Overhead

```bash
# Disable unnecessary services
sudo systemctl disable avahi-daemon
sudo systemctl disable cups

# Free up memory
sudo sync && echo 3 | sudo tee /proc/sys/vm/drop_caches
```

---

## Part 8: Deployment

### 8.1 Create System Service (Optional)

Create `/etc/systemd/system/gesture-control.service`:

```ini
[Unit]
Description=Touchless HCI Gesture Control
After=network.target

[Service]
Type=simple
User=jetson
ExecStart=/home/jetson/arm_challenge/venv/bin/python3 /home/jetson/arm_challenge/step4_gesture_vlc_control.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable gesture-control
sudo systemctl start gesture-control
```

### 8.2 Auto-launch on Boot

Edit `~/.bashrc`:
```bash
# Auto-run gesture control on login
if [[ $DISPLAY ]]; then
    source ~/arm_challenge/venv/bin/activate
    python3 ~/arm_challenge/step4_gesture_vlc_control.py &
fi
```

---

## Part 9: Troubleshooting

### Common Issues

#### 1. MediaPipe Installation Fails
**Error:** `No matching distribution found`

**Solution:**
```bash
# Use pre-built wheel for Jetson
pip install mediapipe-rpi
# or compile from source
git clone https://github.com/google/mediapipe.git
cd mediapipe
python setup.py install
```

#### 2. Low FPS Performance
**Cause:** CPU bottleneck

**Solutions:**
```bash
# Enable GPU acceleration
sudo jetson_clocks

# Reduce image resolution in code
# cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# Reduce detection confidence
min_detection_confidence = 0.5
```

#### 3. VLC Commands Not Working
**Issue:** Gestures detected but VLC not responding

**Solutions:**
```bash
# Verify xdotool works
xdotool key space

# Ensure VLC is in focus
xdotool search --name "VLC media player" windowactivate

# Check VLC is running
pgrep vlc
```

#### 4. Thermal Throttling
**Symptom:** FPS drops after running for a while

**Solution:**
```bash
# Check temperature
cat /sys/class/thermal/thermal_zone0/temp

# Reduce clock speed if needed
sudo nvpmodel -m 1  # Jetson Nano 5W mode (lower power)
sudo nvpmodel -m 0  # High performance mode
```

---

## Part 10: Performance Verification

### 10.1 Run Benchmark

```bash
python3 << 'EOF'
import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

frames = 0
start_time = time.time()

while frames < 100:
    ret, frame = cap.read()
    if not ret:
        break
    
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    frames += 1

elapsed = time.time() - start_time
fps = frames / elapsed

print(f"Processed {frames} frames in {elapsed:.2f}s")
print(f"Average FPS: {fps:.2f}")

cap.release()
EOF
```

### 10.2 Check Gesture Recognition

```bash
# Run with visual feedback
python3 step3_gesture_stability.py

# Perform each gesture 5 times
# Record detection success rate
```

---

## Next Steps

1. ✅ Complete installation
2. ✅ Verify all components working
3. 📖 Read [GESTURE_MAPPING.md](GESTURE_MAPPING.md) for gesture details
4. 🎮 Customize gestures as needed (see README)
5. 📹 Create demo video
6. 📝 Document performance metrics

---

## Additional Resources

- [NVIDIA Jetson Nano Documentation](https://docs.nvidia.com/jetson/jetson-nano/index.html)
- [MediaPipe Installation Guide](https://google.github.io/mediapipe/getting_started/building.html)
- [OpenCV on Jetson](https://docs.opencv.org/master/d6/d15/tutorial_building_tegra.html)
- [Project README](README.md)

---

**Last Updated:** February 2026
