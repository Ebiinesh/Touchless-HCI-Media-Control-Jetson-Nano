# Quick Start Guide

Get up and running with the Touchless HCI Gesture Control system in 5 minutes.

## 1. Prerequisites Check

```bash
# Check if you have Python 3
python3 --version    # Should be 3.6+

# Check if git is installed
git --version

# Verify you're on Jetson Nano
cat /etc/nv_tegra_release
```

## 2. Clone the Repository

```bash
cd ~
git clone https://github.com/yourusername/touchless-hci-gesture-control.git
cd touchless-hci-gesture-control
```

## 3. Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt

# Install system packages
sudo apt install -y xdotool vlc
```

## 4. Test Your Setup

```bash
# Test 1: Hand Tracking (basic)
python3 step1_hand_tracking.py

# Press ESC to exit
```

**Expected:** Camera window opens showing your hand with skeleton overlay

```bash
# Test 2: Finger Counting
python3 step2_finger_count.py

# Raise and lower fingers, press ESC to exit
```

**Expected:** Shows finger count (0-5) in real-time

```bash
# Test 3: Gesture Detection
python3 step3_gesture_stability.py

# Try: Open palm, 2 fingers, 1 finger, fist, press ESC
```

**Expected:** Displays detected gestures (OPEN_PALM, TWO_FINGERS, ONE_FINGER, FIST)

## 5. Run Full System with VLC

### Start VLC with a Media File

```bash
# Option 1: Use a file
vlc ~/Videos/sample.mp4 &

# Option 2: Use a URL
vlc "http://www.example.com/video.mp4" &

# Option 3: Use webcam (for testing)
vlc /dev/video0 &
```

### Run Gesture Control

```bash
python3 step4_gesture_vlc_control.py
```

## 6. Try the Gestures

| Gesture | Action | Try It |
|---------|--------|--------|
| **Open Palm** | Play/Pause | Open all 5 fingers |
| **Two Fingers** | Volume Up | Raise index & middle finger |
| **One Finger** | Volume Down | Raise only index finger |
| **Fist** | Mute | Make a fist |

**Tips:**
- Hold gesture steady for ~1 second
- Maintain good lighting
- Keep hand 50-100cm from camera
- Press ESC to exit

## 7. Troubleshooting

### Camera Not Found
```bash
ls /dev/video*
# Should show /dev/video0 or similar
```

### VLC Not Responding to Gestures
```bash
# Check VLC is running
pgrep vlc

# Test xdotool manually
xdotool key space    # Should play/pause VLC
```

### Low Frame Rate
```bash
# Enable high-performance mode
sudo jetson_clocks

# Rerun the gesture detection
python3 step4_gesture_vlc_control.py
```

### Gesture Not Recognized
- Check lighting (should be bright, not shadowy)
- Make sure fingers are fully extended/closed
- Hold gesture steady for 1+ seconds

## 8. Next Steps

- 📖 Read [README.md](README.md) for full documentation
- 🎯 Check [GESTURE_MAPPING.md](GESTURE_MAPPING.md) for gesture details
- ⚙️ Review [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) for advanced setup
- 📊 See [PERFORMANCE_ANALYSIS.md](PERFORMANCE_ANALYSIS.md) for benchmarks

## 9. Common Commands

```bash
# Deactivate virtual environment
deactivate

# Activate virtual environment (when needed)
source venv/bin/activate

# Stop all Python processes
pkill -f python3

# Kill VLC
pkill vlc

# Check GPU status
nvidia-smi

# Monitor in real-time
watch -n 0.1 nvidia-smi
```

## 10. Project Structure

```
touchless-hci-gesture-control/
├── step1_hand_tracking.py       ← Basic hand tracking
├── step2_finger_count.py        ← Count fingers
├── step3_gesture_stability.py   ← Detect gestures
├── step4_gesture_vlc_control.py ← Full system (use this!)
├── README.md                    ← Full documentation
├── QUICK_START.md              ← This file
└── requirements.txt            ← Dependencies
```

## Support

- **Issues/Bugs:** https://github.com/yourusername/issues
- **Documentation:** Check README.md
- **Installation Help:** See INSTALLATION_GUIDE.md

---

**You're all set! Enjoy touchless media control! 🎮**

