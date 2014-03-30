import cv2

import camera as cam

def main():
  cam.init()

  while(True):
    # Capture frame-by-frame
    img = cam.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

  cam.destroy()

if __name__ == "__main__":
  main()
