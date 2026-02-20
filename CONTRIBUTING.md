# Contributing to Touchless HCI Gesture Control

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

Be respectful, inclusive, and professional in all interactions.

## How to Contribute

### Reporting Bugs

1. **Check existing issues** to avoid duplicates
2. **Create detailed bug report** including:
   - System specifications (Jetson Nano, OS version, JetPack)
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Error messages and logs

Example:
```
Title: Gesture not recognized in low light
OS: JetPack 4.6 on Jetson Nano
Steps:
1. Turn off lights
2. Run step3_gesture_stability.py
3. Perform open palm gesture
Expected: OPEN_PALM detected
Actual: No gesture detected
```

### Suggesting Enhancements

1. **Check discussions** for similar ideas
2. **Describe use case** clearly
3. **Explain expected behavior**
4. **Consider performance impact**

Examples of good enhancement ideas:
- New gesture mappings
- Improved gesture recognition for specific hand positions
- Better error handling
- Performance optimizations
- Documentation improvements

### Submitting Code

#### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/yourusername/touchless-hci-gesture-control.git
cd touchless-hci-gesture-control

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements.txt
pip install black flake8 pytest
```

#### Code Style

Follow PEP 8 guidelines:

```python
# Good
def get_gesture(finger_count):
    """Convert finger count to gesture name."""
    if finger_count == 5:
        return "OPEN_PALM"
    return "UNKNOWN"

# Bad
def getGesture(fc):
    if fc==5: return "OPEN_PALM"
    return "UNKNOWN"
```

Format code:
```bash
black step*.py
flake8 step*.py
```

#### Commit Messages

```
# Good commit messages
git commit -m "Add support for dual-hand gesture recognition"
git commit -m "Fix: Incorrect thumb detection for left hand (fixes #42)"
git commit -m "Docs: Update installation guide for JetPack 5.x"

# Bad commit messages
git commit -m "fix bug"
git commit -m "update"
```

#### Pull Request Process

1. **Fork the repository**
2. **Create feature branch:**
   ```bash
   git checkout -b feature/gesture-name
   ```
3. **Make changes** and test thoroughly
4. **Document changes** in code and README if needed
5. **Commit with clear messages**
6. **Push to your fork:**
   ```bash
   git push origin feature/gesture-name
   ```
7. **Create Pull Request** with:
   - Clear description of changes
   - Reference to related issues
   - Test results/verification
   - Performance impact (if any)

#### Pull Request Checklist

- [ ] Code follows PEP 8 style guide
- [ ] All tests pass
- [ ] New features have documentation
- [ ] Changes are backward compatible
- [ ] Performance impact assessed
- [ ] Commit messages are clear

## Testing

### Running Tests

```bash
# Manual testing steps
python3 step1_hand_tracking.py      # Verify hand detection
python3 step2_finger_count.py       # Verify finger counting
python3 step3_gesture_stability.py  # Verify gesture detection
python3 step4_gesture_vlc_control.py # Verify VLC control
```

### Performance Benchmarking

```bash
python3 << 'EOF'
import cv2
import mediapipe as mp
import time

# Run benchmarks
cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

frames = 0
start = time.time()

while frames < 300:
    ret, frame = cap.read()
    if not ret: break
    result = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    frames += 1

elapsed = time.time() - start
print(f"FPS: {frames / elapsed:.1f}")
EOF
```

## Documentation

### Improving Documentation

- Fix typos in README files
- Clarify confusing sections
- Add examples for common use cases
- Update screenshots/diagrams

### Adding Documentation

When adding new features, document:

1. **What it does** - Clear description
2. **How to use it** - Code examples
3. **Why it matters** - Benefits and use cases
4. **Performance impact** - Latency, FPS, memory
5. **Limitations** - When it doesn't work

## Project Structure

```
├── step1_hand_tracking.py
├── step2_finger_count.py
├── step3_gesture_stability.py
├── step4_gesture_vlc_control.py    ← Main application
├── README.md                        ← Start here
├── GESTURE_MAPPING.md               ← Gesture reference
├── INSTALLATION_GUIDE.md            ← Setup instructions
├── PERFORMANCE_ANALYSIS.md          ← Benchmarks
└── requirements.txt
```

## Release Process

Releases follow semantic versioning: `MAJOR.MINOR.PATCH`

- **MAJOR:** Breaking changes
- **MINOR:** New features (backward compatible)
- **PATCH:** Bug fixes

Example versions:
- v1.0.0 - Initial release
- v1.1.0 - Added dual-hand support
- v1.1.1 - Fixed gesture detection bug

## Getting Help

- **Issues:** Questions about usage → GitHub Discussions
- **Bugs:** Unexpected behavior → GitHub Issues
- **Features:** New ideas → GitHub Issues (label: enhancement)
- **Documentation:** Unclear instructions → Pull request

## Areas for Contribution

### High Priority
- [ ] Improved low-light gesture recognition
- [ ] Dual-hand gesture support
- [ ] Custom gesture training interface
- [ ] Performance optimization for older Jetson models

### Medium Priority
- [ ] Additional VLC control commands
- [ ] Support for other media players (mpv, mplayer)
- [ ] Gesture calibration tool
- [ ] Web UI for settings

### Nice to Have
- [ ] Machine learning-based gesture classifier
- [ ] Gesture recording and playback
- [ ] Performance dashboard
- [ ] Unit tests

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- GitHub contributors list

Thank you for contributing! 🎉

