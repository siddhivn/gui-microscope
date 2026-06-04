# gui-microscope

### What You're Building
A native desktop app on the Pi (PyQt5 window on your monitor) that looks and behaves like a real microscope acquisition GUI. Uses Picamera2 for the Pi Camera and OpenCV for image processing.

### The Full Feature Plan
┌─────────────────────────────────────────┐
│         LIVE PREVIEW (large)            │
│         camera feed, real time          │
├────────────────┬────────────────────────┤
│  CONTROLS      │  IMAGE INFO            │
│                │                        │
│  Exposure      │  Last capture time     │
│  ISO/Gain      │  Resolution            │
│  Brightness    │  Save path             │
│  Contrast      │                        │
│  Resolution    │                        │
├────────────────┴────────────────────────┤
│  [ CAPTURE ]        [ SAVE FOLDER ]     │
└─────────────────────────────────────────┘

### Tech Stack & Why
LibraryRoleWhy not alternativesPyQt5GUI window, layout, widgetsTkinter looks dated, PyQt is what real scientific software usesPicamera2Pi Camera controlOfficial Pi library, works with v1/v2/v3OpenCVFrame conversion, brightness/contrast processingSame library used in real imaging pipelinesPillowImage saving with metadataClean JPEG/PNG saving with timestamps

### Build Phases (in order)
##### Phase 1 — Bare bones window + live preview
Get the camera feed showing in a PyQt window. Nothing else. Just proof it works.
##### Phase 2 — Capture + save
Add a capture button. Saves a timestamped JPEG to a folder.
##### Phase 3 — Controls
Add sliders for exposure, gain, brightness, contrast. Wire them to Picamera2 in real time.
##### Phase 4 — Resolution selector
Dropdown to switch between resolutions. Understand the tradeoff between quality and speed.
##### Phase 5 — Polish
Clean up the layout, add image info panel, folder picker, maybe a capture counter.

Before Writing Any Code — Setup Checklist
Run these on your Pi first:
bash# Update everything
sudo apt update && sudo apt upgrade -y

# Install PyQt5
sudo apt install python3-pyqt5 -y

# Install Picamera2 (may already be installed on recent Pi OS)
sudo apt install python3-picamera2 -y

# Install OpenCV
pip3 install opencv-python --break-system-packages

# Install Pillow
pip3 install Pillow --break-system-packages
Then verify your camera is detected:
bashlibcamera-hello
You should see a preview window open for a few seconds. If that works, you're ready.
