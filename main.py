import cv2
import time
from pose_detection import PoseDetector

def main():
    # Initialize Pose Detector
    detector = PoseDetector()

    # Start capturing video from the webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not access the camera.")
        return

    # Initialize FPS tracker
    prev_time = 0

    # Maximize the window
    cv2.namedWindow("Pose Detection", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Pose Detection", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Detect pose and hand landmarks
        frame = detector.detect_pose_and_hands(frame)

        # Calculate FPS
        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time

        # Display FPS on the frame
        cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display the frame
        cv2.imshow("Pose Detection", frame)

        # Exit on ESC key
        if cv2.waitKey(10) & 0xFF == 27: #27
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()
    detector.close()

if __name__ == "__main__":
    main()
