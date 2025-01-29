import flet as ft
import json
import subprocess

# File to store user settings
CONFIG_FILE = "user_config.json"

# List of all landmark names (based on the provided diagram)
LANDMARKS = [
    "Nose", "Left Eye Inner", "Left Eye", "Left Eye Outer",
    "Right Eye Inner", "Right Eye", "Right Eye Outer",
    "Left Ear", "Right Ear", "Mouth Left", "Mouth Right",
    "Left Shoulder", "Right Shoulder", "Left Elbow", "Right Elbow",
    "Left Wrist", "Right Wrist", "Left Pinky", "Right Pinky",
    "Left Index", "Right Index", "Left Thumb", "Right Thumb",
    "Left Hip", "Right Hip", "Left Knee", "Right Knee",
    "Left Ankle", "Right Ankle", "Left Heel", "Right Heel",
    "Left Foot Index", "Right Foot Index"
]

def save_config(selected_landmarks):
    # Save the selected landmarks to a config file
    with open(CONFIG_FILE, "w") as f:
        json.dump({"selected_landmarks": selected_landmarks}, f)

def start_tracking(e):
    # Collect selected landmarks
    selected_landmarks = [checkbox.label for checkbox in landmark_checkboxes if checkbox.value]
    save_config(selected_landmarks)

    # Run main.py after user selection
    subprocess.Popen(["python", "main.py"])

def main(page: ft.Page):
    page.title = "Landmark Tracker Settings"

    global landmark_checkboxes

    # Create checkboxes for all landmarks
    landmark_checkboxes = [
        ft.Checkbox(label=landmark, value=True) for landmark in LANDMARKS
    ]

    # Add checkboxes to a scrollable container
    scrollable_landmarks = ft.ListView(
        controls=landmark_checkboxes, expand=True, spacing=10
    )

    # Start button to begin tracking
    start_button = ft.ElevatedButton("Start Tracking", on_click=start_tracking)

    # Layout
    page.add(ft.Text("Select Landmarks to Track", size=20, weight="bold"))
    page.add(scrollable_landmarks)
    page.add(start_button)

ft.app(target=main)
