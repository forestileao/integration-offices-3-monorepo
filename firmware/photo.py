import cv2

class CameraController:
  def __init__(self) -> None:
    self.video_capture = cv2.VideoCapture(0)


  def capture_image(self):
    result, video_frame = self.video_capture.read()  # read frames from the video
    if result is False:
        return None

    _, jpeg_binary = cv2.imencode('.jpg', video_frame)

    print("Captured image into JPEG binary")

    return jpeg_binary.tobytes()
