import cv2
import time
import socket
import struct
from pose_detection import PoseDetector

# Set up UDP socket for sending data to Unity
host = '127.0.0.1'  # IP of the Unity application (localhost)
port = 12345  # Port number (make sure this matches Unity's listener)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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

        # Detect full body pose
        frame = detector.detect_pose(frame)

        # Calculate FPS
        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time

        # Send landmarks to Unity
        send_landmarks_to_unity(detector)

        # Display FPS on the frame
        cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display the frame
        cv2.imshow("Pose Detection", frame)

        # Exit on ESC key
        if cv2.waitKey(10) & 0xFF == 27:  # 27 is the ASCII value for ESC
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()
    detector.close()
    sock.close()

def send_landmarks_to_unity(detector):
    # Get the landmarks from the PoseDetector
    landmarks = []
    pose_results = detector.pose_results

    if pose_results.pose_landmarks:
        for landmark in pose_results.pose_landmarks.landmark:
            # Map the normalized coordinates to a reasonable scale for Unity
            x = (landmark.x - 0.5) * 2  # Map to -1, 1 range and spread them
            y = (landmark.y - 0.5) * -2  # Invert and scale Y for Unity's coordinate system
            z = (landmark.z - 0.5) * 2  # Scale Z axis as well, but keep in reasonable range
            landmarks.append((x, y, z))

    # Flatten the landmark list and pack it into a byte string
    data = struct.pack('99f', *[coordinate for landmark in landmarks for coordinate in landmark])

    # Send the packed data to Unity
    sock.sendto(data, (host, port))

if __name__ == "__main__":
    main()
