import cv2

import camera as cam
import visualfx as vis
import display as dis

def main():
  cam.init()

  while(True):
    # Capture frame-by-frame
    img = cam.read()

    # Our operations on the frame come here
    gray = vis.gray(img)

    # Display the resulting frame
    dis.show(gray)

    # Handle key input
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

  # Clean up camera
  cam.destroy()

if __name__ == "__main__":
  main()
