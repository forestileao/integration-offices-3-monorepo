import cv2
import time  # Import the time module for introducing a delay

def capture_picture(cap):
    i = 0
    while i != 10:
        _, frame = cap.read()  # Capture frames from the webcam
        time.sleep(0.1)
        if not _:
            return None  # Return None if frame capture failed
        i += 1
    
    # Return the 10th frame
    return frame

class CameraController:
    def __init__(self) -> None:
        # Initialize the video capture object
        self.video_capture = cv2.VideoCapture(0)
        
        # Introduce a small delay to allow the camera to initialize properly
        time.sleep(2)  # Adjust the delay as needed (e.g., 2 seconds)

    def capture_image(self, savePhoto=False):
        # Capture the 10th frame
        video_frame = capture_picture(self.video_capture)
        if video_frame is None:
            return None  # Return None if frame capture failed
        
        # Convert the captured frame to JPEG binary
        _, jpeg_binary = cv2.imencode('.jpg', video_frame)

        if savePhoto:
            # Save the captured image
            cv2.imwrite('test.jpeg', video_frame)

        print("Captured image into JPEG binary")

        return jpeg_binary.tobytes()


if __name__ == '__main__':
    # Create a CameraController instance
    controller = CameraController()

    # Capture the 10th frame and save it
    controller.capture_image(True)

