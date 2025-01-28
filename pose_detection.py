import mediapipe as mp
import cv2

class PoseDetector:
    def __init__(self):
        # Initialize MediaPipe Pose (only pose detection)
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()

        self.mp_drawing = mp.solutions.drawing_utils

    def detect_pose(self, frame):
        # Convert the frame to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process pose landmarks
        self.pose_results = self.pose.process(frame_rgb)

        # Draw pose landmarks
        if self.pose_results.pose_landmarks:
            self.mp_drawing.draw_landmarks(
                frame,
                self.pose_results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS
            )

        return frame

    def close(self):
        # Release MediaPipe resources
        self.pose.close()
