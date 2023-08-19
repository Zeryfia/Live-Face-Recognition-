import threading
import cv2
from deepface import DeepFace
from tkinter import Tk, filedialog

# Initialize the video capture
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Initialize face_match as a thread-safe boolean
face_match = threading.Event()

# Load the reference image
reference_img = None

# Define a function to load user's own image
def load_reference_image():
    global reference_img
    root = Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(title="Select Reference Image")
    if file_path:
        reference_img = cv2.imread(file_path)
    root.destroy()

# Start by loading the reference image
load_reference_image()

# Define the function to check for a face match
def check_face(frame):
    try:
        verified = DeepFace.verify(frame, reference_img.copy())['verified']
        face_match.set() if verified else face_match.clear()
    except Exception as e:
        print(f"An error occurred: {e}")
        face_match.clear()

# Main loop
counter = 0
while True:
    ret, frame = cap.read()

    if ret:
        if counter % 30 == 0:
            threading.Thread(target=check_face, args=(frame.copy(),)).start()
        counter += 1

        # Display the result
        text = "MATCH!" if face_match.is_set() else "NO MATCH!"
        color = (0, 255, 0) if face_match.is_set() else (0, 0, 255)
        cv2.putText(frame, text, (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, color, 3)
        cv2.imshow('video', frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('l'):
        load_reference_image()

# Release resources and close windows
cap.release()
cv2.destroyAllWindows()
