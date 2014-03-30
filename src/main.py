import cv2

import camera as cam
import visualfx as vis
import display as dis
import homography as hom


def calibrate():
  print 'Calibrate.'
  # get homography
  img = cam.read()
  gray = vis.gray(img)
  H = hom.get_H(gray)
  dis.set_H(H)

def main():
  cam.init()
  #dis.init(1920, 1080)

  while(True):
    # capture frame-by-frame
    img = cam.read()

    # our operations on the frame come here
    gray = vis.gray(img)

    # display the resulting frame
    dis.show(gray)

    # handle key input
    if cv2.waitKey(1) & 0xFF == ord('q'): # quit
        break
    if cv2.waitKey(1) & 0xFF == ord('c'): # calibrate
        calibrate()

  # clean up camera
  cam.destroy()

if __name__ == "__main__":
  main()
