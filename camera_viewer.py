#!/usr/bin/env python3
"""
Raspberry Pi Camera Module 3 with human skeleton tracking using YOLOv8-Pose.
Displays live video feed with detected human poses and skeleton keypoints.
Press 'q' to quit.
"""

import os
from picamera2 import Picamera2
import cv2
from ultralytics import YOLO
import numpy as np

# YOLOv8-Pose keypoint connections (skeleton structure)
# 17 keypoints: nose, eyes, ears, shoulders, elbows, wrists, hips, knees, ankles
SKELETON_CONNECTIONS = [
    [0, 1], [0, 2], [1, 3], [2, 4],  # Head
    [5, 6],  # Shoulders
    [5, 7], [7, 9], [6, 8], [8, 10],  # Arms
    [5, 11], [6, 12],  # Torso
    [11, 13], [13, 15], [12, 14], [14, 16],  # Legs
]

def draw_skeleton(frame, keypoints, confidence_threshold=0.5):
    """
    Draw skeleton on frame from YOLOv8-Pose keypoints.
    
    Args:
        frame: Image frame (BGR format)
        keypoints: Keypoints array from YOLOv8 (shape: [num_people, 17, 3])
                   Each keypoint has [x, y, confidence]
        confidence_threshold: Minimum confidence to draw a keypoint
    """
    if keypoints is None or len(keypoints) == 0:
        return
    
    for person_keypoints in keypoints:
        # Draw keypoints
        for i, (x, y, conf) in enumerate(person_keypoints):
            if conf > confidence_threshold:
                cv2.circle(frame, (int(x), int(y)), 5, (0, 255, 0), -1)
                cv2.circle(frame, (int(x), int(y)), 5, (0, 0, 255), 2)
        
        # Draw skeleton connections
        for connection in SKELETON_CONNECTIONS:
            pt1_idx, pt2_idx = connection
            if (pt1_idx < len(person_keypoints) and pt2_idx < len(person_keypoints)):
                x1, y1, conf1 = person_keypoints[pt1_idx]
                x2, y2, conf2 = person_keypoints[pt2_idx]
                
                if conf1 > confidence_threshold and conf2 > confidence_threshold:
                    cv2.line(frame, 
                            (int(x1), int(y1)), 
                            (int(x2), int(y2)), 
                            (0, 255, 255), 2)

def main():
    # Set display environment variable if not set
    if 'DISPLAY' not in os.environ:
        if os.path.exists('/tmp/.X11-unix'):
            os.environ['DISPLAY'] = ':0'
    
    # Initialize YOLOv8-Pose model
    # Using 'yolov8n-pose.pt' (nano) for better performance on Raspberry Pi
    # Options: yolov8n-pose.pt (nano, fastest), yolov8s-pose.pt (small), yolov8m-pose.pt (medium)
    print("Loading YOLOv8-Pose model...")
    model = YOLO('yolov8n-pose.pt')  # Will download on first run
    print("Model loaded!")
    
    # Initialize the camera
    picam2 = Picamera2()
    
    # Configure camera for preview
    preview_config = picam2.create_preview_configuration(
        main={"size": (1280, 720)}  # Resolution: 1280x720
    )
    picam2.configure(preview_config)
    
    # Start the camera
    picam2.start()
    
    print("Camera started. Tracking human skeletons...")
    print("Press 'q' to quit.")
    
    try:
        while True:
            # Capture frame from camera
            frame = picam2.capture_array()
            
            # Convert RGB to BGR for OpenCV display
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            # Run pose estimation
            results = model(frame_bgr, verbose=False)
            
            # Draw results on frame
            annotated_frame = results[0].plot()  # This draws bounding boxes and keypoints
            
            # Alternative: Custom drawing (uncomment to use custom skeleton drawing)
            # if results[0].keypoints is not None and len(results[0].keypoints.data) > 0:
            #     keypoints = results[0].keypoints.data.cpu().numpy()
            #     draw_skeleton(frame_bgr, keypoints)
            
            # Display the frame
            cv2.imshow("Raspberry Pi Camera - Skeleton Tracking", annotated_frame)
            
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

