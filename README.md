# Raspberry Pi Camera Module 3 Viewer

Basic Python script to capture and display video from Raspberry Pi Camera Module 3.

## Installation

On your Raspberry Pi, install the required dependencies:

```bash
sudo apt update
sudo apt install -y python3-picamera2 python3-opencv
```

## Usage

1. Make sure the camera is connected and enabled:
   ```bash
   sudo raspi-config
   ```
   Navigate to: Interface Options → Camera → Enable

2. Run the script:
   ```bash
   python3 camera_viewer.py
   ```

3. Press 'q' to quit the video viewer.

## Notes

- The script displays video at 1280x720 resolution
- Make sure you're running this on the Raspberry Pi (not via SSH without X11 forwarding)
- If running via SSH, you'll need X11 forwarding enabled: `ssh -X user@raspberry-pi-ip`

