# Raspberry Pi Camera Module 3 - Human Skeleton Tracking

Python script to capture video from Raspberry Pi Camera Module 3 and track human skeletons using YOLOv8-Pose.

## Installation

On your Raspberry Pi, install the required dependencies:

```bash
sudo apt update
sudo apt install -y python3-picamera2 python3-opencv python3-pip

# Install YOLOv8 (Ultralytics)
pip3 install ultralytics
```

**Note:** The YOLOv8 model will be automatically downloaded on first run (yolov8n-pose.pt, ~6MB).

## Usage

1. Make sure the camera is connected and enabled (usually enabled by default on Raspberry Pi 5)

2. Run the script directly on the Raspberry Pi (with display connected):
   ```bash
   python3 camera_viewer.py
   ```

3. The preview window will appear showing the video feed with detected human skeletons. Press `q` to quit.

## Features

- Real-time human pose estimation using YOLOv8-Pose
- Detects 17 keypoints per person (nose, eyes, ears, shoulders, elbows, wrists, hips, knees, ankles)
- Draws skeleton connections between keypoints
- Uses YOLOv8n-Pose (nano) model optimized for Raspberry Pi performance

## Notes

- The script displays video at 1280x720 resolution
- Uses OpenCV for display, which works on the Pi's desktop
- Must be run on the Raspberry Pi itself with a display connected
- The script automatically sets the DISPLAY environment variable if needed
- If running via SSH, you'll need X11 forwarding: `ssh -X user@raspberry-pi-ip`
- Performance: YOLOv8n-Pose should run at ~5-10 FPS on Raspberry Pi 5

