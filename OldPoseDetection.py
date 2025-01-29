import mediapipe as mp
import cv2
class PoseDetector:
    def __init__(self):
        # Initialize MediaPipe Pose and Hands
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()
        
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=False,
                                         max_num_hands=2,
                                         min_detection_confidence=0.7,
                                         min_tracking_confidence=0.7)
        
        self.mp_drawing = mp.solutions.drawing_utils
    def detect_pose_and_hands(self, frame):
        # Convert the frame to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Process pose landmarks
        pose_results = self.pose.process(frame_rgb)
        # Process hand landmarks
        hand_results = self.hands.process(frame_rgb)
        # Draw pose landmarks
        if pose_results.pose_landmarks:
            self.mp_drawing.draw_landmarks(
                frame,
                pose_results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS
            )
        # Draw hand landmarks
        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )
                
                # Extract and display finger tip coordinates
                finger_tips = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky tips
                for tip in finger_tips:
                    x = int(hand_landmarks.landmark[tip].x * frame.shape[1])
                    y = int(hand_landmarks.landmark[tip].y * frame.shape[0])
                    cv2.circle(frame, (x, y), 5, (0, 255, 0), cv2.FILLED)  # Draw circles on finger tips
                    cv2.putText(frame, f"({x}, {y})", (x + 10, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        return frame
    def close(self):
        # Release MediaPipe resources
        self.pose.close()
        self.hands.close()
