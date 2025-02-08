import cv2
import os

def capture_photo() -> str:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Unable to access the camera.")
        return None

    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image.")
        cap.release()
        return None

    photo_path = "desktop_photo.jpg"
    cv2.imwrite(photo_path, frame)
    cap.release()
    print(f"Captured photo and saved to '{photo_path}'.")
    
    return photo_path 