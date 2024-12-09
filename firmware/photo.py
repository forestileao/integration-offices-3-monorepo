import cv2

class CameraController:
  def __init__(self) -> None:
    self.video_capture = cv2.VideoCapture(0)


  def capture_image(self, savePhoto=False):
    result, video_frame = self.video_capture.read()  # read frames from the video
    if result is False:
        return None

    _, jpeg_binary = cv2.imencode('.jpg', video_frame)

    if savePhoto:
      cv2.imwrite('test.jpeg', video_frame)


    print("Captured image into JPEG binary")

    return jpeg_binary.tobytes()


if __name__ == '__main__':
  controller = CameraController()

  controller.capture_image(True)
