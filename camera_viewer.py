#!/usr/bin/env python3
"""
Basic Raspberry Pi Camera Module 3 video viewer.
Displays live video feed from the camera on screen.
Press Ctrl+C to quit.
"""

from picamera2 import Picamera2
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
    
    # Start preview - this displays directly on the Pi's screen
    # Uses QtGL preview which works without X11
    picam2.start_preview()
    
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
        picam2.stop_preview()
        picam2.stop()
        print("Camera stopped.")

if __name__ == "__main__":
    main()

