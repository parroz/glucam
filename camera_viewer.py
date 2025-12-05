#!/usr/bin/env python3
"""
Basic Raspberry Pi Camera Module 3 video viewer.
Displays live video feed from the camera on screen.
Press Ctrl+C to quit.
"""

from picamera2 import Picamera2
from picamera2.previews.qt import QtGlPreview
import time

def main():
    # Initialize the camera
    picam2 = Picamera2()
    
    # Configure camera for preview
    # This creates a low-resolution preview stream
    preview_config = picam2.create_preview_configuration(
        main={"size": (1280, 720)}  # Resolution: 1280x720
    )
    picam2.configure(preview_config)
    
    # Start the camera
    picam2.start()
    
    # Start preview using QtGlPreview - works on Pi's display
    # This creates a preview window that displays on the screen
    preview = QtGlPreview(picam2)
    preview.start()
    
    print("Camera started. Preview displayed on screen.")
    print("Press Ctrl+C to quit.")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
                
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    finally:
        # Clean up
        preview.stop()
        picam2.stop()
        print("Camera stopped.")

if __name__ == "__main__":
    main()

