# Raspberry Pi Camera Module 3 Viewer

Basic Python script to capture and display video from Raspberry Pi Camera Module 3.

## Installation

On your Raspberry Pi, install the required dependencies:

```bash
sudo apt update
sudo apt install -y python3-picamera2
```

## Usage

1. Make sure the camera is connected and enabled (usually enabled by default on Raspberry Pi 5)

2. Run the script directly on the Raspberry Pi (with display connected):
   ```bash
   python3 camera_viewer.py
   ```

3. The preview will appear on the connected screen. Press `Ctrl+C` to quit.

## Notes

- The script displays video at 1280x720 resolution
- Uses picamera2's built-in preview which works directly on the Pi's display (no X11 needed)
- Must be run on the Raspberry Pi itself with a display connected, or via SSH with X11 forwarding
- The preview window will appear on the Pi's desktop/screen

