import cv2
import socket
import json
from pose_detection import PoseDetector  # Import your PoseDetector class

# Initialize the PoseDetector
detector = PoseDetector()

# Socket setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))  # Bind to localhost on port 12345
server_socket.listen(1)

print("Waiting for Unity to connect...")
conn, addr = server_socket.accept()  # Wait for Unity to connect
print(f"Connection established with Unity: {addr}")

# Start capturing video
cap = cv2.VideoCapture(0)  # Open the webcam
if not cap.isOpened():
    print("Error: Could not access the camera.")
    exit()

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Detect pose and hand landmarks
        frame = detector.detect_pose_and_hands(frame)

        # Prepare data to send to Unity
        pose_landmarks = detector.pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).pose_landmarks
        hand_landmarks = detector.hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).multi_hand_landmarks

        # Collect landmarks
        data_to_send = {}

        if pose_landmarks:
            data_to_send['pose'] = [
                {'x': lm.x, 'y': lm.y, 'z': lm.z}
                for lm in pose_landmarks.landmark
            ]

        if hand_landmarks:
            data_to_send['hands'] = []
            for hand in hand_landmarks:
                hand_data = [
                    {'x': lm.x, 'y': lm.y, 'z': lm.z}
                    for lm in hand.landmark
                ]
                data_to_send['hands'].append(hand_data)

        # Send JSON data to Unity
        conn.sendall(json.dumps(data_to_send).encode('utf-8'))

        # Show the frame with landmarks
        cv2.imshow("Pose Detection", frame)

        # Break on ESC key
        if cv2.waitKey(1) & 0xFF == 27:
            break

except Exception as e:
    print(f"Error: {e}")

finally:
    # Clean up resources
    cap.release()
    cv2.destroyAllWindows()
    conn.close()
    server_socket.close()
    detector.close()

# Wait for Unity to connect
print("Waiting for Unity to connect...")
conn, addr = server_socket.accept()  # Accept connection
print(f"Connection established with Unity: {addr}")

# Send a confirmation message to Unity
conn.sendall("Connected to Python server!".encode('utf-8'))
