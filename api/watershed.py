import cv2
import numpy as np

def remove_white_from_image(img):
    # Read the image
    image = img

    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the range for white colors
    lower_white = np.array([20,80,80], dtype=np.uint8)
    upper_white = np.array([255, 255, 255], dtype=np.uint8)

    # Create a mask for white colors
    white_mask = cv2.inRange(hsv, lower_white, upper_white)

    # Apply the mask to the image
    result = cv2.bitwise_and(image, image, mask=white_mask)

    return result

def extract_green(img):
  hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
  greenMask = cv2.inRange(hsv, (26, 65, 100), (105, 250, 255))

  img[greenMask == 255] = (0, 255, 0)

  hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

  lower_green = np.array([35, 40, 40])  # Adjust these values if necessary
  upper_green = np.array([100, 255, 255])

  # Create a mask that isolates the green color
  mask = cv2.inRange(hsv, lower_green, upper_green)

  # Convert single-channel mask to three channels for bitwise operations
  mask3 = cv2.merge([mask, mask, mask])

  # Extract the green region using bitwise AND
  green = cv2.bitwise_and(img, mask3)

  # Convert the original image to grayscale and then back to BGR
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

  # Extract the non-green region
  non_green = cv2.bitwise_and(gray_bgr, cv2.bitwise_not(mask3))

  # Combine the green region with the grayscale non-green region
  #out = cv2.add(non_green, green)

  return green


def apply_watershed(img_binary):
  # CV2
  nparr = np.fromstring(img_binary, np.uint8)
  image = cv2.imdecode(nparr, cv2.IMREAD_COLOR) # cv2.IMREAD_COLOR in OpenCV 3.1
  image = image[90:320, 210:450]
  original = image.copy()

  image = remove_white_from_image(image)
  image = extract_green(image)
  #image grayscale conversion
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  ret, bin_img = cv2.threshold(gray,
                             0, 255,
                             cv2.THRESH_OTSU)
  kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
  bin_img = cv2.morphologyEx(bin_img,
                            cv2.MORPH_OPEN,
                            kernel,
                            iterations=2)

  non_zero_pixels = cv2.countNonZero(bin_img)
  print(f"Number of non-zero pixels: {non_zero_pixels}")
  green_area = non_zero_pixels * 5/1175
  print(f"Green Area: {green_area} cm²")

  # sure background area
  sure_bg = cv2.dilate(bin_img, kernel, iterations=10)

  # Distance transform
  dist = cv2.distanceTransform(bin_img, cv2.DIST_L2, 0)

  #foreground area
  ret, sure_fg = cv2.threshold(dist, 0.1 * dist.max(), 255, cv2.THRESH_BINARY)
  sure_fg = sure_fg.astype(np.uint8)

  # unknown area
  unknown = cv2.subtract(sure_bg, sure_fg)

  # Marker labelling
  # sure foreground
  ret, markers = cv2.connectedComponents(sure_fg)

  # Add one to all labels so that background is not 0, but 1
  markers += 1
  # mark the region of unknown with zero
  markers[unknown == 255] = 0

  # watershed Algorithm
  markers = cv2.watershed(image, markers)

  labels = np.unique(markers)

  leafs = []
  for label in labels[2:]:

  # Create a binary image in which only the area of the label is in the foreground
  #and the rest of the image is in the background
      target = np.where(markers == label, 255, 0).astype(np.uint8)

    # Perform contour extraction on the created binary image
      contours, hierarchy = cv2.findContours(
          target, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
      )
      leafs.append(contours[0])

  # Draw the outline
  img = cv2.drawContours(original, leafs, -1, color=(0, 23, 223), thickness=2)

  _, jpeg_binary = cv2.imencode('.jpg', img)

  return jpeg_binary.tobytes(), green_area, len(labels[2:])
