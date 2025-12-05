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
    print("Loading YOLOv8-Pose model...")
    model = YOLO('yolov8n-pose.pt')  # Will download on first run
    print("Model loaded!")
    
    # Initialize the camera
    picam2 = Picamera2()
    
    # Configure camera for preview - reduced resolution for better performance
    # Lower resolution = faster processing
    preview_config = picam2.create_preview_configuration(
        main={"size": (640, 480)}  # Reduced from 1280x720 for better performance
    )
    picam2.configure(preview_config)
    
    # Start the camera
    picam2.start()
    
    print("Camera started. Tracking human skeletons...")
    print("Press 'q' to quit.")
    print("Performance optimizations: Lower resolution, frame skipping, smaller model input")
    
    # Performance optimization: Process every Nth frame
    # Higher number = better FPS but less frequent pose updates
    FRAME_SKIP = 2  # Process every 2nd frame (adjust: 1=every frame, 2=every 2nd, 3=every 3rd)
    frame_count = 0
    last_results = None
    
    try:
        while True:
            # Capture frame from camera
            frame = picam2.capture_array()
            
            # Convert RGB to BGR for OpenCV display
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            # Only run inference every Nth frame for better performance
            if frame_count % FRAME_SKIP == 0:
                # Run pose estimation with optimized settings
                # imgsz=320: smaller input size = faster inference
                # half=True: use FP16 if available (faster on some hardware)
                # device='cpu': explicitly use CPU (or 'cuda' if GPU available)
                results = model(frame_bgr, 
                              imgsz=320,  # Smaller input size for faster processing
                              verbose=False,
                              device='cpu')
                last_results = results[0]
            
            # Use last results for display (smooth video even when skipping frames)
            if last_results is not None:
                # Draw results on frame
                annotated_frame = last_results.plot()  # This draws bounding boxes and keypoints
            else:
                annotated_frame = frame_bgr
            
            # Display the frame
            cv2.imshow("Raspberry Pi Camera - Skeleton Tracking", annotated_frame)
            
            frame_count += 1
            
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

