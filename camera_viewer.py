#!/usr/bin/env python3
"""
Basic Raspberry Pi Camera Module 3 video viewer.
Displays live video feed from the camera on screen.
Press 'q' to quit.
"""

import os
from picamera2 import Picamera2
import cv2

def main():
    # Set display environment variable if not set
    # This helps OpenCV find the display when running on Pi's desktop
    if 'DISPLAY' not in os.environ:
        # Try common display values for Raspberry Pi
        if os.path.exists('/tmp/.X11-unix'):
            os.environ['DISPLAY'] = ':0'
    
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
    
    print("Camera started. Press 'q' to quit.")
    
    try:
        while True:
            # Capture frame from camera
            frame = picam2.capture_array()
            
            # Convert RGB to BGR for OpenCV display (OpenCV uses BGR)
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            # Display the frame
            cv2.imshow("Raspberry Pi Camera", frame_bgr)
            
            # Check for 'q' key press to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    finally:
        # Clean up
        picam2.stop()
        cv2.destroyAllWindows()
        print("Camera stopped.")

if __name__ == "__main__":
    main()

